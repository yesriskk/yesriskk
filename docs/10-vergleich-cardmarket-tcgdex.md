# 10 – Vergleich: Cardmarket-Download vs. TCGdex

Grundlage: `price_guide_6.json` und beide Produktkataloge vom 2026-09-04 sowie ein Clone von `tcgdex/cards-database` inklusive Server-Code (Stand 2026-09-04).

## Der wichtigste Befund

**TCGdex hat keine eigene Preisquelle.** Der Server lädt stündlich exakt die Datei `downloads.s3.cardmarket.com/productCatalog/priceGuide/price_guide_6.json`, legt sie nach `idProduct` in einen Cache und gibt für jede Karte, die in der TCGdex-Datenbank eine `thirdParty.cardmarket`-ID trägt, die Zeile unverändert zurück (plus `updated` und `unit: "EUR"`, ohne `idCategory`). Die Cardmarket-Preise von TCGdex sind also eine **Teilmenge** des Downloads, nie mehr. Alles, was TCGdex zusätzlich hat, ist Katalog, nicht Preis.

## Gegenüberstellung

| Aspekt | Cardmarket-Download | TCGdex |
|---|---|---|
| **Was es ist** | Preisliste + Produktkatalog des Marktplatzes | Karten-Datenbank mit Metadaten und Bildern, Preise durchgereicht |
| Einzelkarten-Produkte | 73.195 (jede Sprache eigenes Produkt) | 23.641 international + 18.217 Asien = 41.858 Karten, je Karte alle Sprachen in einem Datensatz |
| Sets/Expansions | 774 Expansions (Set × Sprache) | 221 internationale + 343 asiatische Sets |
| Sealed-Produkte | 5.048 in 11 Kategorien, mit Preisen | praktisch keine |
| Preisfelder EUR | avg, low, trend, avg1, avg7, avg30, jeweils + Reverse-Holo | dieselben Felder, nur für Karten mit Cardmarket-ID |
| Karten mit EUR-Preis | 73.195 Produkte (davon ~64.000 mit Trend) | 30.802 Karten (20.207 intl + 10.595 Asien) |
| **Preise pro Sprache** | ja, DE/EN/FR/JP/… getrennt | nein, eine ID pro Karte (international: englische Expansion, Asien: japanische) |
| Preise USD | nein | ja, TCGplayer über tcgcsv (19.982 intl + 6.360 Asien Karten mit ID) |
| Preis-Historie | nein (nur 1/7/30-Tage-Schnitt) | nein |
| Aktualisierung | täglich ~02:45 MESZ | stündlicher Abruf derselben Datei |
| Kartenname | "Name [Attacke 1 \| Attacke 2]", nur englisch | lokalisiert: en 23.548, fr 22.023, de 20.897, it 15.615, es 15.468, pt 14.362, ko 1.124; Asien: ja 13.223, th 2.994, id 2.788 |
| Kartennummer, Seltenheit | nein | ja (Nummer im Dateinamen, `rarity` bei allen 23.641 intl Karten) |
| Attacken, Fähigkeiten, HP, Typ, Stage, Schwächen, Rückzug | nur Attackennamen im Produktnamen | vollständig, lokalisiert (attacks 19.917, abilities 4.386, hp 20.110 intl) |
| Illustrator, Regulation Mark, Pokédex-Nr. | nein | ja (illustrator 23.106, regulationMark 8.293, dexId 20.019 intl) |
| Varianten (normal/reverse/holo/1st Ed.) | implizit über `*-holo`-Felder | explizit als `variants`-Objekt (15.074 intl Karten), `variants_detailed` mit eigenen IDs im Aufbau |
| Bilder | keine | pro Sprache über assets.tcgdex.net, `low`/`high`, png/webp/jpg |
| Expansion-Namen | nein (nur ID) | Set-Namen lokalisiert, Abkürzungen, Release-Datum, Kartenanzahl, Set-Logo/Symbol |
| Verknüpfung zueinander | `idProduct`, `idExpansion` | `thirdParty.cardmarket` an Karte (30.802) und Set (209) |
| Zugang | öffentlicher Download, kein Key | REST/GraphQL, kein Key; Datenbank Open Source (MIT), self-hostbar |
| Zuverlässigkeit | Cardmarket selbst | Community-Projekt, Pflegerückstand bei 2025/26-Sets (Cardmarket-IDs nur bei 12–23 % der neuen Karten) |

## Was Cardmarket mehr hat

1. **Sprachgetrennte Preise.** Eine deutsche Glurak-Karte hat auf Cardmarket einen anderen Preis als die englische. TCGdex liefert nur einen davon.
2. **Doppelt so viele bepreiste Produkte** (73.195 vs. 30.802), weil TCGdex nur gemappte Karten bepreisen kann.
3. **Sealed-Preise** für 5.048 Produkte.
4. **Kontrolle über den Zeitpunkt.** Wir lesen die Datei direkt nach Erstellung, nicht wann TCGdex sie zuletzt geholt hat.

## Was TCGdex mehr hat

1. **Alles, was eine Karte ausmacht:** lokalisierte Namen, Nummern, Seltenheit, Attacken, Bilder, Set-Struktur. Ohne das gibt es keinen Katalog, keine Suche, keinen Scanner und kein Master-Set.
2. **USD-Preise** (TCGplayer).
3. **Das Mapping-Seed** `thirdParty.cardmarket` für 30.802 Karten und 209 Sets.
4. **Varianten-Modell**, das wir für Reverse/Holo/1st Edition übernehmen können.

## Entscheidung: was wir benutzen

| Bedarf | Quelle | Begründung |
|---|---|---|
| Karten-Katalog, Sets, Namen in allen Sprachen, Nummern, Seltenheit, Attacken | **TCGdex** (Datenbank-Clone oder API) | einzige Quelle dafür |
| Kartenbilder pro Sprache | **TCGdex** Assets-CDN | einzige Quelle |
| EUR-Preise Einzelkarten, pro Sprache | **Cardmarket-Download direkt** | Obermenge von TCGdex, sprachgetrennt, ohne Zwischenstation |
| EUR-Preise Sealed | **Cardmarket-Download** (`nonsingles` + Price Guide) | TCGdex hat nichts |
| USD-Preise | **TCGdex** `pricing.tcgplayer` (oder später tcgcsv direkt) | Cardmarket hat nichts |
| Preis-Historie | **eigene tägliche Snapshots** aus dem Cardmarket-Download | keine Quelle hat Historie |
| ID-Mapping Cardmarket ↔ Karte | **TCGdex-Seed** + eigene Pipeline (`08-id-mapping.md`) | Seed deckt 40,7 % der Produkte, Rest selbst |
| TCGdex-`pricing.cardmarket` in der App | **nicht verwenden** | redundant zum Download, nur eine Sprache, weniger Abdeckung |

## Konsequenzen für Architektur und Roadmap

- `packages/pricing`: Provider `cardmarket` liest die Download-Datei, Provider `tcgplayer` liest TCGdex (USD). Kein `tcgdex`-Provider für EUR.
- Katalog-Import: statt der TCGdex-API den **Datenbank-Clone** (`tcgdex/cards-database`, MIT) einlesen. Das gibt uns `thirdParty`-IDs, alle Sprachen und Attacken in einem Durchlauf ohne Rate-Limits; die API bleibt für Bilder-URLs und als Referenz.
- Datenmodell: `cardmarket_expansions(id_expansion, tcgdex_set_id, language)`; Preisabfrage pro Sammlungs-Item über (`card_id`, `language`) → `idProduct`.
- Beitrag zurück: fehlende `thirdParty.cardmarket`-IDs, die unsere Pipeline findet, als PR an TCGdex. Das verbessert deren USD/EUR-Kopplung und unser Seed für neue Sets.
