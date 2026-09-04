# 08 – ID-Mapping Cardmarket ↔ TCGdex

Ergebnis der Analyse vom 2026-09-04 mit `price_guide_6.json`, `products_singles_6.json`, `products_nonsingles_6.json` und einem Clone von `tcgdex/cards-database` (MIT). Reproduzierbar mit `tools/analysis/cardmarket_mapping_probe.py`.

## Was die Produktkataloge enthalten

Felder in beiden Dateien: `idProduct`, `name`, `idCategory`, `categoryName`, `idExpansion`, `idMetacard`, `dateAdded`.

**Die Annahme "Set-Kürzel und Nummer stehen im Namen" ist falsch.** Einzelkarten heißen `Name [Attacke 1 | Attacke 2]` (Pokémon, 55.398 Stück) oder nur `Name` (Trainer/Energie, 16.613), plus 1.184 Code-Karten. Es gibt keine Kartennummer, keine Seltenheit, keine Sprache und keine Expansion-Namen (nur `idExpansion`, 774 Expansions bei Singles). `idMetacard` gruppiert Nachdrucke derselben Karte über Expansions hinweg (16.762 Metacards).

| Kategorie | Anzahl | Name |
|---|---|---|
| 51 | 73.195 | Pokémon Single |
| 1015 | 1.103 | Pokémon Box Set |
| 52 | 786 | Pokémon Booster |
| 1017 | 681 | Pokémon Coins |
| 53 | 617 | Pokémon Display |
| 1014 | 571 | Pokémon Tins |
| 54 | 559 | Pokémon Theme Decks |
| 1083 | 495 | Pokémon Blisters |
| 1016 | 170 | Pokémon Elite Trainer Boxes |
| 1064 | 28 | Pokémon Lot |
| 1654 | 25 | PCG Set |
| 1013 | 13 | Pokémon Trainer Kits |

**Das Kernproblem:** 10.193 Gruppen mit identischem Namen innerhalb einer Expansion (24.500 Zeilen, ein Drittel aller Singles). Das sind Regular-, Full-Art-, Illustration-Rare- und Secret-Versionen derselben Karte, die aus der Datei allein nicht unterscheidbar sind.

## Der Durchbruch: TCGdex trägt Cardmarket-IDs

Die TCGdex-Datenbank (Open Source, MIT) hat in Karten- und Set-Dateien ein Feld `thirdParty.cardmarket`. Damit:

| Kennzahl | Wert |
|---|---|
| Karten mit Cardmarket-ID in TCGdex | 29.789 (19.196 international, 10.591 Asien) |
| Singles im Cardmarket-Katalog dadurch gemappt | 29.787 von 73.195 (40,7 %) |
| Trend-wertgewichtete Abdeckung | 28,6 % |
| Karten mit Trend ≥ 20 € gemappt | 2.490 von 6.885 |
| Cardmarket-Expansions gemappt | 265 von 774, davon 250 sauber 1:1 |

Die Abdeckung ist bei alten Sets hoch (Karten vor 2015: 84 %) und bei 2025/26 niedrig (23 % bzw. 12 %). Das ist ein Pflegerückstand bei TCGdex, kein strukturelles Problem: Wir können unser Mapping dorthin zurückspielen (Beitrag an ein MIT-Projekt, das wir ohnehin nutzen).

## Zweiter Hebel: Produkt-ID-Reihenfolge entspricht Kartennummer

In den 3.339 vollständig gemappten Namensdubletten-Gruppen entspricht die aufsteigende `idProduct`-Reihenfolge in **94,8 %** der Fälle der aufsteigenden Kartennummer. Ausnahmen sind fast nur e-Card-Sets (Aquapolis/Skyridge mit H-Nummern). Damit lassen sich Dubletten in modernen Sets auflösen: Sortiere die Gruppe nach `idProduct`, sortiere die TCGdex-Kandidaten mit gleichem Namen nach Nummer, ordne paarweise zu.

## Was übrig bleibt

43.408 Singles ohne TCGdex-ID, davon 36.509 in 493 Expansions ohne jede Zuordnung. Namens-Überlappung dieser Expansions mit TCGdex-Sets:

| Beste Jaccard-Ähnlichkeit | Expansions | Karten |
|---|---|---|
| ≥ 0,8 | 29 | 2.705 |
| 0,6–0,8 | 20 | 1.766 |
| 0,4–0,6 | 42 | 4.125 |
| < 0,4 | 402 | 27.913 |

**Bestätigt (2026-09-04):** Die nicht gemappten Expansions, die bereits gemappten Sets ähneln, sind **sprachspezifische Editionen** desselben Sets. Cardmarket führt pro Sprache eine eigene Expansion mit eigenen Produkt-IDs und damit eigenen Preisen. Das ist für uns ein Vorteil: Wir bekommen **sprachgetrennte Preise** (z. B. deutsche vs. englische vs. japanische Karte) und müssen sie nur auf dasselbe TCGdex-Set mit Sprachattribut mappen. `cardmarket_expansions` bekommt deshalb die Spalten `tcgdex_set_id` und `language`, und `card_external_ids` wird pro (`card_id`, `language`) geführt. Preisabfragen in der App wählen die Expansion passend zur Sprache des Sammlungs-Items, mit Fallback auf EN.

## Mapping-Pipeline für Phase 0

1. **Seed:** `thirdParty.cardmarket` aus TCGdex für Karten und Sets importieren → `card_external_ids` mit `confidence = 1.0`, `source = 'tcgdex'`.
2. **Expansion-Mapping vervollständigen:** (a) aus Nonsingles-Namen ableiten ("Phantom Forces Booster" → Expansion 1521 = Phantom Forces, geht für 410 Expansions), (b) Namens-Jaccard ≥ 0,6 gegen TCGdex-Sets in allen Sprachen, (c) Sprachvarianten erkennen: mehrere Expansions mit fast identischer Kartenliste = ein Set in mehreren Sprachen; welche Sprache welche ist, muss einmalig auf cardmarket.com nachgesehen werden, (d) Rest manuell in `cardmarket_expansions(id_expansion, tcgdex_set_id, language, verified)`. 774 Zeilen sind manuell in wenigen Stunden schaffbar.
3. **Karten-Mapping pro Expansion:** Basisname + Attackennamen gegen TCGdex-Karten des Sets in der Sprache der Expansion (TCGdex hat Namen und Attacken lokalisiert; Cardmarket-Namen sind auch bei fremdsprachigen Expansions englisch, daher primär EN matchen und Sprache aus der Expansion-Tabelle übernehmen); eindeutig → `confidence 0.9`; Dubletten per `idProduct`-Reihenfolge → `confidence 0.7`; Rest → Review-Queue.
4. **Review-UI** (kleines internes Tool oder Tabelle): Kandidaten nebeneinander mit TCGdex-Bild, Bestätigung setzt `confidence 1.0`.
5. **Qualitätsmetrik im Worker:** Anteil gemappter Singles und trend-gewichtete Abdeckung täglich loggen; Ziel vor Phase 1: ≥ 90 % der Karten mit Trend ≥ 5 €.
6. **Rückgabe an TCGdex:** gemappte IDs als PR gegen `cards-database`, damit das Mapping öffentlich gepflegt wird und `variants_detailed` uns später entlastet.

## Konsequenzen für das Datenmodell

- `cardmarket_products` speichert den Katalog roh inklusive `idMetacard` und `idExpansion`.
- `cardmarket_expansions` ist eine eigene, manuell kuratierte Tabelle mit Sprachattribut.
- `card_external_ids(card_id, source, external_id, confidence, method, verified_by, verified_at)`; `method` ∈ {`tcgdex-seed`, `name-attacks`, `order`, `manual`}.
- Preis-Snapshots werden **immer** gegen `idProduct` gespeichert, auch ohne Mapping. Historie geht nie verloren, ein späteres Mapping macht sie rückwirkend sichtbar.
