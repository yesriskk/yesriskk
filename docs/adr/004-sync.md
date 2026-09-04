# ADR-004: Sync zwischen iPhone und Mac

- Status: **Angenommen** (2026-09-04)
- Datum: 2026-09-04
- Entscheider: Dev A, Dev B

## Kontext

Ein Nutzer arbeitet abwechselnd am Mac (Scanner, Massenerfassung) und am iPhone (Kamera, Alarme, Portfolio unterwegs). Beide Geräte müssen denselben Stand zeigen, Änderungen sollen ohne manuelles "Aktualisieren" ankommen, und das iPhone soll auch ohne Netz die Sammlung anzeigen und Änderungen vormerken.

## Optionen

1. **Supabase als Quelle der Wahrheit + lokaler Cache + Outbox + Realtime** (eigener, schlanker Sync)
   - Jede Nutzertabelle hat `id (uuid, clientseitig erzeugt)`, `user_id`, `updated_at`, `deleted_at` (Soft-Delete), `device_id`.
   - Client hält eine SQLite-Kopie (GRDB) und eine **Outbox** mit ausstehenden Änderungen. Online: Outbox sofort per Upsert an Supabase; offline: bleibt liegen, wird beim nächsten Verbinden gesendet.
   - **Pull:** Delta-Abfrage `where updated_at > last_sync` pro Tabelle; **Push:** Upsert der Outbox.
   - **Live:** Supabase Realtime (Postgres Changes) auf den eigenen Zeilen (`user_id = auth.uid()`); eingehende Änderung → lokal anwenden → UI aktualisiert sich. Ein am Mac gescannter Stapel erscheint innerhalb ~1 s auf dem iPhone.
   - **Konflikte:** Last-Write-Wins pro Zeile über `updated_at` (Server-Zeit). Für `quantity` optional Mengen-Delta statt Absolutwert, damit gleichzeitige +1 auf zwei Geräten nicht verloren geht.
   - Pro: keine zusätzliche Infrastruktur, alles mit Supabase-Bordmitteln; gut verstanden; Datenmodell bleibt normales Postgres.
   - Contra: Sync-Code selbst schreiben und testen (Property-Tests für Merge-Logik).
2. **PowerSync** (Sync-Dienst, offiziell mit Supabase integriert, Swift-SDK vorhanden)
   - Übernimmt Delta-Sync, Outbox, Konflikte, Offline-Queue. Server-seitige Sync-Rules definieren, was pro Nutzer repliziert wird.
   - Pro: reifer als Eigenbau, Swift- und JS-SDK, gute Supabase-Doku.
   - Contra: zusätzlicher Dienst (Cloud oder self-hosted), Free-Tier begrenzt, ab ~49 USD/Monat; weitere Abhängigkeit für ein Zwei-Personen-Projekt.
3. **CloudKit** (Apples Sync)
   - Verworfen: bindet Daten an iCloud-Account, keine Server-Auswertung (Portfolio, Alarme) möglich, Supabase wäre trotzdem nötig.

## Entscheidung

**Option 1** für v1. Der Sync-Umfang ist überschaubar (Sammlung, Sealed, Wishlist, Binder, Verkäufe, Einstellungen), die Nutzer sind meist online, und Realtime liefert das "sofort auf dem anderen Gerät"-Gefühl. Sollte die Merge-Logik in Phase 1 mehr als zwei Wochen fressen, wechseln wir auf PowerSync (Option 2), das Datenmodell ist dafür bereits passend.

## Konsequenzen

- Alle Nutzertabellen: `id uuid default gen_random_uuid()`, `user_id`, `created_at`, `updated_at` (Trigger setzt Server-Zeit), `deleted_at`, `device_id`. RLS auf `user_id`.
- Realtime für `collection_items`, `sealed_items`, `wishlist_items`, `binders`, `sales` aktivieren; Publikation auf diese Tabellen beschränken.
- Fotos: Upload in Storage zuerst, dann Zeile mit Pfad; Download lazy auf dem anderen Gerät.
- Sync-Modul lebt in `PokeVaultKit` (Swift) mit Tests gegen eine lokale Supabase; Merge-Logik deterministisch und mit Property-Tests abgesichert.
- Nutzer kann mehrere Geräte haben; `device_id` dient nur Diagnose, nicht Berechtigung.
