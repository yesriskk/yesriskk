# 01 – Feature-Katalog

Priorisierung nach MoSCoW: **M** = Must (MVP), **S** = Should (v1.0), **C** = Could (v1.x), **W** = Won't (vorerst nicht).
Die Spalte *Phase* verweist auf die Roadmap in `04-roadmap.md`.

## A. Sammlung erfassen

| # | Feature | Prio | Phase | Anmerkungen |
|---|---|---|---|---|
| A1 | Karten-Katalog durchsuchen (Set, Name, Nummer, Sprache, Variante) | M | 1 | Basis für alles. Quelle: TCGdex. |
| A2 | Karte manuell zur Sammlung hinzufügen (Menge, Zustand, Sprache, Variante, Kaufpreis, Kaufdatum) | M | 1 | Zustand nach Cardmarket-Skala (MT/NM/EX/GD/LP/PL/PO). |
| A3 | **Scanner: Einzelkarte per Foto** | M | 2 | Erkennung on-device über perzeptuelle Hashes + OCR-Tiebreaker (siehe Architektur). |
| A4 | **Bulk-Scanner: Live-Kamera/Video, Karten nacheinander hinhalten** | S | 3 | Kontinuierliche Frame-Verarbeitung, Auto-Add bei stabilem Match, Undo-Stack. |
| A5 | Scan-Review-Queue: unsichere Treffer mit Top-3-Kandidaten bestätigen | S | 2 | Verhindert Falscheinträge im Bulk-Modus. |
| A6 | Sealed-Produkte erfassen (Booster Box, ETB, Display, Tins, Blister) | S | 3 | Optional per EAN-Barcode-Scan. |
| A7 | Import aus CSV / anderen Apps (Cardmarket-Wants, Collectr, TCG Collector) | C | 4 | Mapping-Assistent. |
| A8 | Graded Karten erfassen (Grader, Grade, Cert-Nummer, Sub-Grades) | S | 3 | Cert-Nummer verlinkt auf Grader-Verifikation. |
| A9 | Sammlung / Einzelkarte "Kollektion" vs. "Investment" vs. "Zum Verkauf" taggen | S | 3 | Frei definierbare Tags + drei System-Tags. |

## B. Preise und Markt

| # | Feature | Prio | Phase | Anmerkungen |
|---|---|---|---|---|
| B1 | Aktuelle Preise in EUR (Cardmarket-Referenz: Trend, Avg, Low, 7d/30d) | M | 1 | Über TCGdex; direkter Cardmarket-API-Zugang ist für Neubewerber geschlossen (siehe `02-data-sources.md`). |
| B2 | Preise in USD (TCGplayer) als Zweitwährung | S | 1 | Kommt im selben Datensatz mit. |
| B3 | **Eigene Preis-Historie** (Tag/Woche/Monat/Jahr) | M | 1 | Wir snapshotten täglich ab Tag 1. Je früher Phase 1 live geht, desto länger die Historie. |
| B4 | Preis-Charts pro Karte mit Zeitraum-Umschalter | M | 1 | 24h / 7d / 30d / 90d / 1y / All. |
| B5 | Graded-Preise (PSA 10/9/8, CGC, BGS, TAG) | S | 3 | Nur Bezahlquellen (Scrydex, PriceCharting) oder manuell gepflegte Comps. |
| B6 | Verkäufe pro Tag / Liquidität | C | 4 | Keine offene Quelle für Cardmarket-Sales; eBay Marketplace Insights ist gesperrt. Anfangs: Proxy über Anzahl Angebote / Preisbewegung. |
| B7 | Winner & Loser der eigenen Sammlung (24h / 7d / 30d / 90d) | S | 2 | Absolut und prozentual, Filter nach Set/Tag. |
| B8 | Markt-Movers global (Top-Steiger/-Faller über alle Karten) | C | 4 | Discovery-Feature, gut für Retention. |
| B9 | Wishlist mit Preis-Wecker (unter X € / über X € / -Y % in 7d) | S | 2 | Push-Notifications. |
| B10 | Verkaufs-Alarme für eigene Karten (Take-Profit, Stop-Loss-Warnung) | C | 3 | Gleiche Alarm-Engine wie B9. |
| B11 | Multi-Currency (EUR/USD, Umrechnung mit Tageskurs) | S | 1 | ECB-Kurse. |

## C. Portfolio und Investment

| # | Feature | Prio | Phase | Anmerkungen |
|---|---|---|---|---|
| C1 | Portfolio-Gesamtwert + Entwicklung über die Zeit | M | 1 | Tägliche Portfolio-Snapshots (Wert, Anzahl, Cost-Basis). |
| C2 | Unrealized / Realized P&L, ROI, pro Karte und gesamt | S | 3 | Braucht Kaufpreis (A2) und Verkaufs-Erfassung (D3). |
| C3 | Cost-Basis-Methoden (FIFO/Durchschnitt) | C | 4 | Für Mehrfachkäufe derselben Karte. |
| C4 | Investment-Tracking für Sealed (Kaufpreis, MSRP, Entwicklung) | S | 3 | Preisquelle für Sealed ist dünner als für Singles. |
| C5 | Allokation (nach Set, Ära, Sprache, Sealed vs. Singles, Graded vs. Raw) | C | 3 | Donut-Charts. |
| C6 | Wochen-/Monatsreport als Push oder E-Mail | C | 4 | "Deine Sammlung ist diese Woche +3,2 %." |
| C7 | Wert-Gutachten / Versicherungs-Export (PDF mit Bildern und Preisen) | C | 4 | Für Hausrat-Versicherung. |

## D. Verkaufen und Handeln

| # | Feature | Prio | Phase | Anmerkungen |
|---|---|---|---|---|
| D1 | **eBay-Listing automatisieren** (Titel, Bilder, Preis-Vorschlag, Kategorie, Versandprofil) | S | 4 | eBay Sell/Inventory API, OAuth pro Nutzer, Business Policies nötig. |
| D2 | Cardmarket-Listing | W→C | – | Keine API für uns. Bestenfalls Deep-Link/Clipboard-Export. |
| D3 | Verkauf erfassen (Plattform, Preis, Gebühren, Käufer-Land) → Realized P&L | S | 3 | Manuell zuerst, später eBay-Sync über Fulfillment API. |
| D4 | Tauschliste / Duplikate ("Habe doppelt") und Freunde-Vergleich | C | 4 | Social-Layer; auch als Public-Profile-Link. |
| D5 | Preis-Vorschlag beim Listen (Cardmarket-Trend vs. eBay-Comps) | C | 4 | Hängt an B5/B6. |

## E. Grading

| # | Feature | Prio | Phase | Anmerkungen |
|---|---|---|---|---|
| E1 | **Grading-Guide**: Grader-Vergleich (PSA, CGC, BGS, TAG, AP Grading, PCA, …), Kosten-Tiers, Turnaround, Einreichung aus DE/EU | S | 3 | Redaktioneller Inhalt in der DB (CMS-artig), damit Preise ohne App-Update aktualisiert werden können. |
| E2 | **Grading-ROI-Rechner**: Raw-Preis vs. erwarteter Graded-Preis × Wahrscheinlichkeit je Grade − Kosten | S | 3 | Zeigt Break-even-Grade. Braucht B5. |
| E3 | "Lohnt sich"-Liste über die eigene Sammlung (höchstes Graded/Raw-Verhältnis) | S | 3 | Direkt aus E2 abgeleitet. |
| E4 | Pregrading-Check: Foto-Checkliste (Ecken, Kanten, Oberfläche, Zentrierung) mit Kamera-Overlay | C | 3 | Zentrierungs-Messung per Randerkennung ist realistisch; ML-Grade-Schätzung ist Forschungsthema (später). |
| E5 | Submission-Tracker: eingereicht wann, wo, Status, Kosten, Ergebnis | C | 4 | Kosten fließen in C2. |
| E6 | Population-Reports (wie viele PSA 10 existieren) | C | 4 | Scrydex liefert das, sonst manuell. |

## F. Sammlung organisieren

| # | Feature | Prio | Phase | Anmerkungen |
|---|---|---|---|---|
| F1 | **Master-Set-Tracker** pro Set: Fortschritt %, fehlende Karten, Kosten bis Komplettierung | S | 2 | "Master" = inkl. Reverse Holos und Secret Rares; konfigurierbar. |
| F2 | Virtuelle Binder (Seiten 3×3 / 4×3, Drag-and-drop, Sortierung nach Nummer) | S | 2 | Spiegelt physische Binder. |
| F3 | Kartenbilder in der jeweiligen Sprache (DE/EN/JP/FR/…) | M | 1 | TCGdex liefert pro Sprache. Fallback auf EN. |
| F4 | Zustand, Variante (Holo/Reverse/1st Ed./Promo-Stempel), Notizen, eigene Fotos | M | 1 | Eigene Fotos in Object Storage. |
| F5 | Set-Kalender / Release-Übersicht | C | 4 | Aus Katalogdaten. |
| F6 | Share-Bild (Karte + Preis + Entwicklung als Grafik für Instagram/WhatsApp) | C | 4 | Viraler Kanal. |
| F7 | Offline-Modus und Multi-Device-Sync | M | 1 | Lokale DB + Sync. |

## G. Plattform / Delight

| # | Feature | Prio | Phase | Anmerkungen |
|---|---|---|---|---|
| G1 | **Dynamic Island / Live Activity** mit wählbarem Pokémon-Icon (Portfolio-Ticker, Preisalarm, Scan-Session) | C | 3 | iOS 16.1+, nativer Widget-Extension-Code (Swift). Live Activities laufen max. 8 h aktiv + 4 h stale, sind also kein Dauer-Widget. Icon-Set muss unter 30 MB bleiben. |
| G2 | Alternative App-Icons (Pokémon-Motive) | C | 3 | Trivial umzusetzen, gute Ergänzung zu G1. |
| G3 | Home-Screen-Widgets (Portfolio-Wert, Top-Mover, Wishlist-Alarm) | C | 3 | WidgetKit; Android-Widgets später. |
| G4 | Push-Notifications (Alarme, Reports) | S | 2 | |
| G5 | Achievements ("Erstes Master-Set", "100 Karten gescannt") | C | 4 | Retention. |
| G6 | Öffentliches Sammler-Profil (Read-only-Link) | C | 4 | |

## Bewusst gestrichen / verschoben

- **Cardmarket-Listing-Automatisierung**: ohne API nicht sauber machbar.
- **Automatische Grade-Schätzung per KI**: Als Forschungs-Spike nach v1.0, nicht als Versprechen.
- **Eigene Preis-Berechnung aus Rohdaten (Scraping)**: rechtlich und wartungstechnisch nicht tragbar.
