# 02 – Datenquellen

Stand der Recherche: September 2026. Bitte vor Phase 0 nochmal gegenprüfen, APIs in diesem Markt ändern sich schnell.

## Zusammenfassung

| Bedarf | Empfehlung | Kosten | Status |
|---|---|---|---|
| Karten-Katalog + Bilder (mehrsprachig) | **TCGdex** | kostenlos, Open Source | ✅ primär |
| Aktuelle Preise EUR (Cardmarket) | **Cardmarket Price Guide Download** (offizielle Tagesdatei, ohne API) | kostenlos | ✅ primär |
| Preise USD (TCGplayer) + EUR-Fallback | **TCGdex `pricing`-Feld** | kostenlos | ✅ sekundär |
| Sealed-Preise EUR | **Cardmarket Produktkatalog `nonsingles` + Price Guide** | kostenlos | ✅ Phase 3 |
| Preis-Historie | **Eigene tägliche Snapshots** | eigene Infrastruktur | ✅ ab Phase 1 |
| Graded-Preise, Population | **Scrydex** (Growth-Tier) oder **PriceCharting** | ab ~29 $/Monat bzw. Abo | ⏳ Phase 3, Entscheidung offen |
| Verkäufe pro Tag / Sold Comps | keine offene Quelle | – | ❌ Phase 4, Proxy-Metriken |
| Wechselkurse | ECB / frankfurter.app | kostenlos | ✅ |
| Grader-Kosten & -Infos | redaktionell gepflegt (eigene Tabelle) | – | ✅ |
| eBay Listing | eBay Sell APIs (Inventory, Account, Fulfillment) | kostenlos, Developer-Account | ✅ Phase 4 |

## 1. Cardmarket: API zu, Daten trotzdem offen

**API:** Die offizielle Cardmarket-API nimmt keine neuen Bewerbungen an (Hilfeseite: "not accepting applications"). Bestehende Zugänge dürfen nicht mit Dritt-Apps geteilt werden. **Scraping** von cardmarket.com verstößt gegen die AGB und ist technisch fragil. Kommerzielle Drittanbieter mit "Cardmarket-Daten" (cardmarket-api.com, tcgapis.com u. a.) haben intransparente Herkunft und sind nur Fallback.

**Offene Downloads (unser Hauptweg):** Cardmarket hat den Price Guide und den Produktkatalog, die früher nur API-Nutzern zugänglich waren, für alle zum Download freigegeben (News: "We're Making the Price Guide and Product Catalogue Available for Download"). Einstiegsseite: `https://www.cardmarket.com/en/Pokemon/Data/Price-Guide` (bzw. `/de/Pokemon/Data/Price-Guide`). Bekannte Dateipfade (Pokémon = `idGame` 6):

| Datei | Inhalt |
|---|---|
| `downloads.s3.cardmarket.com/productCatalog/priceGuide/price_guide_6.json` (auch als CSV) | Täglicher Price Guide (**verifiziert**): pro `idProduct` `avg`, `low`, `trend`, `avg1`, `avg7`, `avg30` sowie dieselben Werte für die Reverse-Holo-Variante als `*-holo`; `avg1/7/30` nur bei Einzelkarten |
| `downloads.s3.cardmarket.com/productCatalog/productList/products_singles_6.json` | Alle Einzelkarten (**verifiziert**, 73.195): `idProduct`, `name`, `idCategory`, `categoryName`, `idExpansion`, `idMetacard`, `dateAdded` |
| `downloads.s3.cardmarket.com/productCatalog/productList/products_nonsingles_6.json` | Alle Sealed-Produkte (**verifiziert**, 5.048 in 11 Kategorien), gleiche Felder |

Was die Dateien **nicht** enthalten: Bilder, lokalisierte Namen, Kartennummer, Seltenheit, Expansion-Namen, Preise nach Zustand oder Sprache, Verkaufszahlen, Historie über den 30-Tage-Schnitt hinaus.

**Verifiziert am 2026-09-04** anhand einer echten `price_guide_6.json`: Struktur, Felder und Datenqualität stehen in `07-cardmarket-price-guide.md`. Kurz: 78.243 Produkte, davon 73.195 Einzelkarten, Preise als `avg/low/trend/avg1/avg7/avg30` plus Reverse-Holo-Spiegel `*-holo`, Erzeugung täglich ~02:45 MESZ.

**Rechtlicher Status der Download-Dateien (Stand 2026-09-04, siehe Abschnitt 8a):** Die Dateien sind für alle Nutzer frei herunterladbar. Die Cardmarket-AGB enthalten aber für die API eine Klausel, nach der die *Darstellung von Karten und Preisen* eine vorherige schriftliche Zustimmung erfordert. Ob diese Klausel auch die Download-Dateien erfasst, ist offen. **Vor einem öffentlichen Release holen wir eine schriftliche Zustimmung von Cardmarket ein** (Entwurf in `docs/09-cardmarket-anfrage.md`). Interne Entwicklung und Snapshot-Sammlung sind davon nicht blockiert.

**Vor Phase 0 noch prüfen (von einem Rechner mit Zugriff auf cardmarket.com):**
1. Steht auf der Data-Seite ein eigener Nutzungshinweis oder ein Verweis auf die AGB? Text oder Screenshot in `08a` unten ablegen.
2. Anfrage an Cardmarket absenden (siehe `09`).

**Konsequenz:** Der Cardmarket-Download wird Provider Nr. 1 für EUR-Preise, direkt von der Quelle, inklusive Sealed. TCGdex bleibt Katalog-, Bild- und USD-Quelle sowie EUR-Fallback. Das Preis-Modul bleibt quellenneutral (`price_source`-Spalte).

**Mapping Cardmarket `idProduct` ↔ TCGdex `card_id`:** Die Produktnamen enthalten **keine** Kartennummer (Muster `Name [Attacke | Attacke]`). Der Hauptweg ist deshalb das Feld `thirdParty.cardmarket`, das TCGdex in seiner Open-Source-Datenbank pflegt (deckt 40,7 % der Singles ab), ergänzt um Name-plus-Attacken-Matching und die Beobachtung, dass die `idProduct`-Reihenfolge in 95 % der Fälle der Kartennummer folgt. Details, Zahlen und Pipeline in `08-id-mapping.md`.

## 2. TCGdex (Katalog + Preise + Bilder)

- REST + GraphQL, kein API-Key, Open Source (self-hostbar, falls Rate-Limits stören).
- Sprachen: EN, DE, FR, ES, IT, PT, JA, KO, ZH u. a. Bilder pro Sprache, Qualität `low`/`high`, Format `png`/`webp`/`jpg`.
- IDs sind stabil (`swsh3-136`), das wird unser `card_id`.
- Preise: `pricing.cardmarket` (EUR) und `pricing.tcgplayer` (USD). Ein geplantes Feld `variants_detailed` wird direkte Cardmarket-/TCGplayer-IDs pro Variante liefern → beobachten.
- Lücken: Sealed-Produkte werden nur rudimentär abgedeckt (dafür Cardmarket `nonsingles`); Sprach-Preise sind Cardmarket-übergreifend. TCGdex' Cardmarket-Werte stammen sehr wahrscheinlich aus denselben öffentlichen Price-Guide-Dateien, sind also kein zweiter unabhängiger Datenpunkt.

**Import-Strategie:** Einmaliger Voll-Import aller Sets/Karten in unsere Postgres-Tabelle `cards` (alle Sprachen), danach täglicher Delta-Lauf (neue Sets) + täglicher Preis-Lauf.

## 3. Preis-Historie: selbst bauen

Keine kostenlose Quelle liefert mehrjährige Cardmarket-Historie. Deshalb:

- Cron-Job **täglich** (Uhrzeit nach Cardmarket-Update-Zeitpunkt): Price-Guide-Datei laden, über das ID-Mapping in `price_snapshots(card_id, variant, source, currency, captured_on, avg, low, trend, avg1, avg7, avg30)` schreiben; zweiter Lauf für TCGdex (USD + Fallback).
- Die Cardmarket-Rohdatei (~wenige MB) zusätzlich unverändert im Storage archivieren (`raw/cardmarket/price_guide_6_YYYY-MM-DD.json`). Kostet fast nichts und erlaubt späteres Neu-Mapping ohne Datenverlust.
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
- Cardmarket veröffentlicht keine Verkaufszahlen; der Price Guide enthält nur Preisaggregate, keine Volumina.
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

## 8a. Cardmarket-Nutzungsbedingungen: was wir wissen

Quelle: Cardmarket General Terms and Conditions, Abschnitt zur API (Wortlaut aus Suchtreffern, Originalseite aus der Entwicklungsumgebung nicht abrufbar, bitte gegenprüfen):

> "Cardmarket provides registered users with a permanent Access Token which enables access and partly to edit their own inventory data as well as publicly accessible data via an application programming interface (API). […] The API may only be used for managing your own contents. **The presentation of the trading cards and their respective prices require prior written agreement.** The use of the API and the transfer and use of data for any other purpose is prohibited. Access via the API is an additional offer provided by Cardmarket which is exclusively intended to facilitate the use of the online platform."

Aus der Hilfeseite zur API: Bewerbungen für API-Zugang werden derzeit nicht angenommen; kommerzielle App-Entwickler konnten früher auf Anfrage einen "App Key" erhalten; API-Zugangsdaten dürfen nicht an Dritt-Apps weitergegeben werden.

Aus der News-Ankündigung zu den Downloads: Price Guide und Produktkatalog sind "for all users" herunterladbar, der Price Guide täglich, der Katalog bei neuen Releases; die entsprechenden API-Endpunkte wurden mit Einführung der Dateien abgekündigt. Eine eigene Lizenz oder ein expliziter Verwendungszweck für die Dateien wurde in den Suchergebnissen nicht gefunden.

**Bewertung (keine Rechtsberatung):**
- Die AGB-Klausel bezieht sich wörtlich auf die API. Cardmarket hat die Dateien aber genau als Ersatz für diese API-Endpunkte veröffentlicht; es ist plausibel, dass Cardmarket dieselbe Erwartung an die Nutzung hat.
- Unabhängig von den AGB gilt in der EU das **Datenbankherstellerrecht** (§§ 87a ff. UrhG, Datenbank-Richtlinie 96/9/EG): Die tägliche Entnahme des gesamten Price Guides ist eine Entnahme eines "wesentlichen Teils" und braucht eine Erlaubnis. Das öffentliche Anbieten zum Download ist ein starkes Indiz für eine konkludente Erlaubnis zum Herunterladen, sagt aber nichts über die Weiterverbreitung in einer App.
- Marktpraxis: Mehrere Sammler-Apps zeigen "Cardmarket-Preise" an. Ob mit schriftlicher Vereinbarung, ist von außen nicht erkennbar.
- **Konsequenz:** Wir behandeln die Anzeige von Cardmarket-Preisen in der App als zustimmungspflichtig, bis Cardmarket schriftlich etwas anderes sagt. Bis dahin: entwickeln, Snapshots sammeln, nicht veröffentlichen. Bei Ablehnung: TCGdex-Preise anzeigen (TCGdex trägt dann das Quellenrisiko) oder auf Bezahl-APIs ausweichen; die eigene Historie bleibt erhalten, weil sie gegen `idProduct` gespeichert ist.

## 8. Rechtliches

- **Pokémon-IP:** Keine offiziellen Logos/Wordmarks, kein "Pokémon" im App-Namen. Kartenbilder werden von TCGdex gehostet; wir cachen nur Thumbnails und verweisen auf die Quelle. Disclaimer "nicht affiliiert mit Nintendo/Creatures/GAME FREAK/The Pokémon Company" in App und Store.
- **Nutzerdaten:** DSGVO (EU-Hosting, Auskunft/Löschung, Datenschutzerklärung). Fotos der eigenen Karten sind personenbezogene Daten des Nutzers → Verschlüsselung at rest, Löschung bei Account-Löschung.
- **API-ToS:** TCGdex-Attribution in der App; Bezahl-APIs verbieten meist Weitergabe der Rohdaten → wir zeigen abgeleitete Werte.
