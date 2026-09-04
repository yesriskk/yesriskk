# 02 – Datenquellen

Stand der Recherche: September 2026. Bitte vor Phase 0 nochmal gegenprüfen, APIs in diesem Markt ändern sich schnell.

## Zusammenfassung

| Bedarf | Empfehlung | Kosten | Status |
|---|---|---|---|
| Karten-Katalog + Bilder (mehrsprachig) | **TCGdex** | kostenlos, Open Source | ✅ primär |
| Aktuelle Preise EUR (Cardmarket) + USD (TCGplayer) | **TCGdex `pricing`-Feld** | kostenlos | ✅ primär |
| Preis-Historie | **Eigene tägliche Snapshots** | eigene Infrastruktur | ✅ ab Phase 1 |
| Graded-Preise, Population | **Scrydex** (Growth-Tier) oder **PriceCharting** | ab ~29 $/Monat bzw. Abo | ⏳ Phase 3, Entscheidung offen |
| Verkäufe pro Tag / Sold Comps | keine offene Quelle | – | ❌ Phase 4, Proxy-Metriken |
| Wechselkurse | ECB / frankfurter.app | kostenlos | ✅ |
| Grader-Kosten & -Infos | redaktionell gepflegt (eigene Tabelle) | – | ✅ |
| eBay Listing | eBay Sell APIs (Inventory, Account, Fulfillment) | kostenlos, Developer-Account | ✅ Phase 4 |

## 1. Cardmarket – die unbequeme Wahrheit

- Die **offizielle Cardmarket-API nimmt keine neuen Bewerbungen an** (Hilfeseite: "not accepting applications"). Bestehende Zugänge dürfen nicht mit Dritt-Apps geteilt werden.
- **Scraping** von cardmarket.com verstößt gegen die AGB und ist technisch fragil (Cloudflare). Kein Weg für uns.
- Es gibt kommerzielle Drittanbieter, die "Cardmarket-Daten" per API verkaufen (cardmarket-api.com, tcgapis.com, cardmarketapi.com). Deren Datenherkunft ist nicht transparent, rechtlich grau, und die Anbieter können jederzeit verschwinden. **Nur als Fallback, nicht als Fundament.**
- **Praktischer Weg:** TCGdex liefert in jedem Kartenobjekt ein `pricing.cardmarket`-Objekt (EUR: avg, low, trend, avg1/avg7/avg30, jeweils normal + holo/reverse) mit täglicher Aktualisierung. Damit bekommen wir "Preise via Cardmarket" ohne eigene Cardmarket-Integration.

**Konsequenz:** Wir bauen das Preis-Modul quellenneutral (`price_source`-Spalte) und hängen TCGdex als erste Quelle dran. Sollte später ein Cardmarket-Zugang möglich werden, ist das ein zusätzlicher Provider, kein Umbau.

## 2. TCGdex (Katalog + Preise + Bilder)

- REST + GraphQL, kein API-Key, Open Source (self-hostbar, falls Rate-Limits stören).
- Sprachen: EN, DE, FR, ES, IT, PT, JA, KO, ZH u. a. Bilder pro Sprache, Qualität `low`/`high`, Format `png`/`webp`/`jpg`.
- IDs sind stabil (`swsh3-136`), das wird unser `card_id`.
- Preise: `pricing.cardmarket` (EUR) und `pricing.tcgplayer` (USD). Ein geplantes Feld `variants_detailed` wird direkte Cardmarket-/TCGplayer-IDs pro Variante liefern → beobachten.
- Lücken: Sealed-Produkte werden nur rudimentär abgedeckt; Sprach-Preise sind Cardmarket-übergreifend (Cardmarket unterscheidet Preise nach Sprache nur bedingt).

**Import-Strategie:** Einmaliger Voll-Import aller Sets/Karten in unsere Postgres-Tabelle `cards` (alle Sprachen), danach täglicher Delta-Lauf (neue Sets) + täglicher Preis-Lauf.

## 3. Preis-Historie: selbst bauen

Keine kostenlose Quelle liefert mehrjährige Cardmarket-Historie. Deshalb:

- Cron-Job **täglich um 06:00 UTC**: alle Karten mit Preisen abrufen, in `price_snapshots(card_id, variant, source, currency, captured_on, avg, low, trend, avg7, avg30)` schreiben.
- Ab ~20.000 Karten × 2 Varianten × 365 Tage ≈ 15 Mio Zeilen/Jahr → Postgres mit Partitionierung nach Monat reicht locker. Optional später TimescaleDB.
- Portfolio-Snapshots pro Nutzer täglich aus den Preis-Snapshots aggregieren (`portfolio_snapshots`).
- **Deshalb ist Phase 1 zeitkritisch:** Jeder Tag ohne Snapshot ist ein Tag ohne Historie. Der Snapshot-Job ist das allererste Backend-Stück, das live geht, noch vor der App.
- Bootstrap: Für die ersten Wochen kann `avg7`/`avg30` aus TCGdex genutzt werden, um rückwirkend grobe Punkte zu interpolieren (klar als "geschätzt" markiert).

## 4. Graded-Preise

| Anbieter | Was | Kosten | Bewertung |
|---|---|---|---|
| **Scrydex** (Team hinter pokemontcg.io) | Graded-Preise (PSA/BGS/CGC), Historie, Population; USD; Cardmarket "in Evaluierung" | kein Free-Tier, ab 29 $/Monat, Graded ab Growth-Tier (99 $/Monat) | beste Datentiefe, aber USD-zentriert |
| **PriceCharting** | PSA 10 / 9 / 8, Ungraded, Sealed; USD; Historie | API im Abo | gut für Sealed + Graded, weniger präzise bei Varianten |
| Manuell / Community | Eigene Comps-Tabelle, von uns/Nutzern gepflegt | 0 € | MVP-tauglich für Top-200-Karten |

**Empfehlung:** Phase 3 mit PriceCharting *oder* Scrydex-Growth starten (Entscheidung nach Trial, siehe `06-risks.md`). EUR-Graded-Preise = USD × Tageskurs, deutlich als Näherung gekennzeichnet.

## 5. Verkäufe pro Tag / Sold Comps

- eBay **Marketplace Insights API** (sold items) ist "restricted, not open to new users". Die Finding API ist abgeschaltet. Eingeloggt-Pflicht für Sold-Filter auf ebay.com seit 08/2026.
- Cardmarket veröffentlicht keine Verkaufszahlen.
- **Realistisch:** Liquiditäts-Proxy aus (a) Anzahl aktiver Angebote (falls die Quelle das liefert), (b) Preisvolatilität, (c) eigenen Verkaufsdaten der Nutzer (aggregiert, anonymisiert). Als "Aktivitäts-Score" statt "Verkäufe/Tag" labeln, damit wir nichts versprechen, was die Daten nicht hergeben.

## 6. eBay Sell APIs (Listing-Automatisierung)

- Developer-Programm kostenlos; Sandbox vorhanden.
- Pro Nutzer OAuth-Consent (User Token), Business Policies (Versand/Retoure/Zahlung) und Inventory Location sind Pflicht, sonst kein `publishOffer`.
- Flow: `createOrReplaceInventoryItem` → `createOffer` → `publishOffer`. Bilder müssen über HTTPS erreichbar sein (unser Storage).
- Verkaufs-Sync über Fulfillment API (`getOrders`) → automatisches Realized-P&L.
- Marktplatz `EBAY_DE`, Kategorie "Sammelkartenspiele/TCG" mit Pflicht-Item-Specifics (Spiel, Sprache, Zustand, Kartennummer …).

## 7. Grader-Daten (Grading-Guide)

Eigene Tabelle `graders` + `grader_service_tiers` (Grader, Tier, Preis, max. Deklarationswert, Turnaround, Versandhinweise DE/EU, Link). Redaktionell gepflegt, Quelle jeweils verlinken. Stand 2026 relevant für DE:

- PSA (USA; über Vermittler ~105–113 €/Karte Regular; Economy ~18–25 $ + Versand; **PSA Frankfurt** ab Sommer 2026, entfällt EU-Einfuhr-USt-Problem).
- CGC, BGS (USA, ähnlich über Vermittler).
- TAG (USA, KI-gestützt, transparent).
- AP Grading (DE, ab 19,90 €, 5 Werktage), PCA (FR), Pure Grading (EU) – günstiger, geringerer Wiederverkaufs-Aufschlag.

## 8. Rechtliches

- **Pokémon-IP:** Keine offiziellen Logos/Wordmarks, kein "Pokémon" im App-Namen. Kartenbilder werden von TCGdex gehostet; wir cachen nur Thumbnails und verweisen auf die Quelle. Disclaimer "nicht affiliiert mit Nintendo/Creatures/GAME FREAK/The Pokémon Company" in App und Store.
- **Nutzerdaten:** DSGVO (EU-Hosting, Auskunft/Löschung, Datenschutzerklärung). Fotos der eigenen Karten sind personenbezogene Daten des Nutzers → Verschlüsselung at rest, Löschung bei Account-Löschung.
- **API-ToS:** TCGdex-Attribution in der App; Bezahl-APIs verbieten meist Weitergabe der Rohdaten → wir zeigen abgeleitete Werte.
