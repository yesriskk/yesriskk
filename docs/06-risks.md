# 06 – Risiken und offene Entscheidungen

## Offene Entscheidungen (als ADR festhalten)

| ADR | Frage | Optionen | Empfehlung | Bis wann |
|---|---|---|---|---|
| 001 | Client-Stack (iOS + Desktop) | Expo + Tauri vs. native Swift (iOS + macOS) vs. Flutter | Expo + Tauri, sofern Windows-Desktop nicht ausgeschlossen ist | Phase 0, Woche 1 |
| 003 | Mac-Scanner-Anbindung | – | **Angenommen:** ImageCaptureCore + Ordner-Import | erledigt |
| 002 | Backend | Supabase vs. eigenes Postgres + Node-API | Supabase + separater Worker | Phase 0, Woche 1 |
| 003 | Graded-Preisquelle | PriceCharting vs. Scrydex vs. manuell | Trial beider in Phase 2, Entscheidung vor Phase 3 | Ende Phase 2 |
| 004 | Sync iPhone ↔ Mac | – | **Angenommen:** eigener Sync (Cache + Outbox + Realtime), PowerSync als Ausweichplan | erledigt |
| 005 | App-Name & Branding | – | Name ohne "Pokémon", Markenrecherche; bestimmt Bundle-ID, GitHub-Org, Package-Name | vor Phase 0 |
| 006 | Monetarisierung | kostenlos / Pro-Abo (Graded-Preise, Bulk-Scan, eBay) / einmalig | Freemium mit Pro-Abo, da Bezahl-APIs laufende Kosten verursachen | vor Phase 3 |

## Risiken

| Risiko | Wahrscheinlichkeit | Auswirkung | Gegenmaßnahme |
|---|---|---|---|
| **TCGdex ändert Preisfeld oder fällt aus** | mittel | hoch | Provider-Abstraktion; Self-Hosting-Option von TCGdex (Open Source); Fallback-Provider evaluieren; eigene Snapshots bleiben erhalten |
| **Cardmarket widerspricht später der Nutzung der Download-Dateien** (AGB-Klausel gilt nach unserer Lesart nur für die API) | niedrig | hoch | Quelle nennen und verlinken; Anfrage-Entwurf (`09`) bereithalten; Fallback Bezahl-API; Historie bleibt, weil gegen `idProduct` gespeichert |
| **Cardmarket stellt die offenen Price-Guide-Downloads ein oder ändert die Bedingungen** | niedrig-mittel | hoch | Rohdateien archivieren; TCGdex als Fallback-Provider fertig halten; kein Scraping |
| **ID-Mapping Cardmarket ↔ TCGdex unvollständig** (Promos, JP-Karten, Varianten) | hoch | mittel | Automatik + Review-Tabelle, Abdeckung als Metrik im Worker, TCGdex `variants_detailed` beobachten |
| **Scanner-Trefferquote unter 95 %** (Glanz, Beleuchtung, Reverse Holo, JP-Karten) | mittel | hoch | Früh Feldtest (Phase 2), Review-Queue als Sicherheitsnetz, OCR-Tiebreaker, später Embedding-Fallback |
| **Offline-Sync-Bugs** (Duplikate, verlorene Edits) | mittel | hoch | Fertige Sync-Lösung ernsthaft prüfen (ADR-004); Property-based Tests für Merge-Logik |
| **Bezahl-APIs kosten laufend Geld** (Scrydex 29–99 $/Monat) | sicher | mittel | Erst ab Phase 3, gekoppelt an Monetarisierung (ADR-006); Caching, nur Karten mit Nutzer-Interesse abfragen |
| **eBay-API-Review / Business-Policy-Hürden** | mittel | mittel | Sandbox früh, Feature als "Pro"; Fallback: vorbereitetes Listing per Clipboard |
| **Pokémon-IP / App-Store-Ablehnung** | niedrig-mittel | hoch | Kein offizielles Branding, Disclaimer, eigene Icons für Dynamic Island |
| **Zwei-Personen-Projekt verliert Momentum** | mittel | hoch | Kleine Milestones, M0 nach 2 Wochen, eigene Sammlung als Motivation, wöchentlicher Sync |
| **Logik doppelt (Swift-Client, TS-Worker) driftet auseinander** | mittel | mittel | Berechnungen ins Backend (Views/RPC); Hash-Algorithmus mit gemeinsamen Testvektoren; generierte Swift-Typen aus `packages/shared` |
| **macOS-CI-Minuten teuer** | sicher | niedrig | Xcode Cloud (25 h/Monat im Developer Program enthalten) statt GitHub-macOS-Runner |
| **Große Claude-Diffs kollidieren** | mittel | mittel | Paketgrenzen, Contract-first, kleine PRs, worktrees |
| **Live Activities enttäuschen** (8-h-Limit, kein Dauer-Widget) | hoch | niedrig | Erwartung im Feature klar kommunizieren; Home-Widget als "Dauer-Anzeige" |
| **Scanner-Modell der Devs wird von macOS nicht erkannt** oder liefert schlechte Scans | niedrig (Gerät 2–3 Jahre alt) | mittel | Test: erscheint das Gerät in Apples "Digitale Bilder"-App? Dann funktioniert ImageCaptureCore. Ordner-Import als garantierter Fallback |
| **App-Store-Ablehnung wegen Pokémon-Marke** (Guideline 5.2) | mittel | hoch | Neutraler Name, eigene Grafiken, Disclaimer, keine offiziellen Assets; Ablehnung einplanen (eine Runde) |
| **Speicher/Performance bei 15 Mio Snapshot-Zeilen/Jahr** | niedrig | mittel | Partitionierung, Aggregat-Tabellen (Wochen-/Monatswerte), Retention-Policy für Tagesdaten > 2 Jahre |
