# 06 – Risiken und offene Entscheidungen

## Offene Entscheidungen (als ADR festhalten)

| ADR | Frage | Optionen | Empfehlung | Bis wann |
|---|---|---|---|---|
| 001 | Mobile-Stack | Expo/RN vs. native SwiftUI vs. Flutter | Expo/RN (Cross-Platform, ein Stack, Claude-freundlich) | Phase 0, Woche 1 |
| 002 | Backend | Supabase vs. eigenes Postgres + Node-API | Supabase + separater Worker | Phase 0, Woche 1 |
| 003 | Graded-Preisquelle | PriceCharting vs. Scrydex vs. manuell | Trial beider in Phase 2, Entscheidung vor Phase 3 | Ende Phase 2 |
| 004 | Offline-Sync-Strategie | eigener Sync (updated_at/soft-delete) vs. PowerSync/WatermelonDB/ElectricSQL | Prototyp beider in Phase 1, Woche 1 | Phase 1, Woche 2 |
| 005 | App-Name & Branding | – | Name ohne "Pokémon", Markenrecherche | Phase 1 |
| 006 | Monetarisierung | kostenlos / Pro-Abo (Graded-Preise, Bulk-Scan, eBay) / einmalig | Freemium mit Pro-Abo, da Bezahl-APIs laufende Kosten verursachen | vor Phase 3 |

## Risiken

| Risiko | Wahrscheinlichkeit | Auswirkung | Gegenmaßnahme |
|---|---|---|---|
| **TCGdex ändert Preisfeld oder fällt aus** | mittel | hoch | Provider-Abstraktion; Self-Hosting-Option von TCGdex (Open Source); Fallback-Provider evaluieren; eigene Snapshots bleiben erhalten |
| **Cardmarket verweigert die schriftliche Zustimmung zur Preisanzeige** (AGB: "presentation of … prices require prior written agreement") | mittel | hoch | Anfrage früh stellen (`09-cardmarket-anfrage.md`); bis zur Antwort nicht veröffentlichen; Fallback TCGdex-Preise oder Bezahl-API; Historie bleibt, weil gegen `idProduct` gespeichert |
| **Cardmarket stellt die offenen Price-Guide-Downloads ein oder ändert die Bedingungen** | niedrig-mittel | hoch | Rohdateien archivieren; TCGdex als Fallback-Provider fertig halten; kein Scraping |
| **ID-Mapping Cardmarket ↔ TCGdex unvollständig** (Promos, JP-Karten, Varianten) | hoch | mittel | Automatik + Review-Tabelle, Abdeckung als Metrik im Worker, TCGdex `variants_detailed` beobachten |
| **Scanner-Trefferquote unter 95 %** (Glanz, Beleuchtung, Reverse Holo, JP-Karten) | mittel | hoch | Früh Feldtest (Phase 2), Review-Queue als Sicherheitsnetz, OCR-Tiebreaker, später Embedding-Fallback |
| **Offline-Sync-Bugs** (Duplikate, verlorene Edits) | mittel | hoch | Fertige Sync-Lösung ernsthaft prüfen (ADR-004); Property-based Tests für Merge-Logik |
| **Bezahl-APIs kosten laufend Geld** (Scrydex 29–99 $/Monat) | sicher | mittel | Erst ab Phase 3, gekoppelt an Monetarisierung (ADR-006); Caching, nur Karten mit Nutzer-Interesse abfragen |
| **eBay-API-Review / Business-Policy-Hürden** | mittel | mittel | Sandbox früh, Feature als "Pro"; Fallback: vorbereitetes Listing per Clipboard |
| **Pokémon-IP / App-Store-Ablehnung** | niedrig-mittel | hoch | Kein offizielles Branding, Disclaimer, eigene Icons für Dynamic Island |
| **Zwei-Personen-Projekt verliert Momentum** | mittel | hoch | Kleine Milestones, M0 nach 2 Wochen, eigene Sammlung als Motivation, wöchentlicher Sync |
| **Große Claude-Diffs kollidieren** | mittel | mittel | Paketgrenzen, Contract-first, kleine PRs, worktrees |
| **Live Activities enttäuschen** (8-h-Limit, kein Dauer-Widget) | hoch | niedrig | Erwartung im Feature klar kommunizieren; Home-Widget als "Dauer-Anzeige" |
| **Speicher/Performance bei 15 Mio Snapshot-Zeilen/Jahr** | niedrig | mittel | Partitionierung, Aggregat-Tabellen (Wochen-/Monatswerte), Retention-Policy für Tagesdaten > 2 Jahre |
