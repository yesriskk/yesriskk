# 07 – Cardmarket Price Guide: verifiziertes Schema

Geprüft anhand der Datei `price_guide_6.json`, `createdAt` 2026-09-04 02:44 (MESZ), 15 MB, 78.243 Produkte. Die Datei selbst liegt **nicht** im Repo (Größe, Nutzungsbedingungen noch nicht geklärt).

## Struktur

```json
{
  "version": 1,
  "createdAt": "2026-09-04T02:44:38+0200",
  "priceGuides": [
    {
      "idProduct": 271439, "idCategory": 52,
      "avg": 99.99, "low": 85, "trend": 344.42,
      "avg1": null, "avg7": null, "avg30": null,
      "avg-holo": null, "low-holo": null, "trend-holo": 3.93,
      "avg1-holo": null, "avg7-holo": null, "avg30-holo": null
    }
  ]
}
```

| Feld | Bedeutung | Hinweis |
|---|---|---|
| `idProduct` | Cardmarket-Produkt-ID | eindeutig, unser Schlüssel für `card_external_ids` |
| `idCategory` | Produkttyp | 51 = Einzelkarten (73.195), übrige = Sealed/Zubehör (siehe unten) |
| `avg`, `low`, `trend` | Durchschnitts-, niedrigster, Trendpreis in EUR | für alle Kategorien |
| `avg1`, `avg7`, `avg30` | 1/7/30-Tage-Verkaufsdurchschnitt | **nur bei Einzelkarten befüllt**, bei Sealed immer `null` |
| `*-holo` | dieselben Werte für die Reverse-Holo-Variante | Schlüssel fehlt bei ~9.200 Produkten komplett (kein Reverse existiert) |

Alle Preise sind EUR mit zwei Nachkommastellen, `null` = keine Daten. Die Datei wird täglich gegen 02:45 MESZ erzeugt → Snapshot-Job auf **04:00 MESZ (02:00 UTC)** legen, mit Retry bis 08:00, und `createdAt` als `captured_on`-Quelle verwenden (nicht die Abrufzeit).

## Kategorien (idCategory)

| id | Anzahl | Vermutung (mit Produktkatalog verifizieren) |
|---|---|---|
| 51 | 73.195 | Einzelkarten |
| 52 | 786 | Booster |
| 53 | 617 | Displays / Booster Boxes |
| 54 | 559 | Themendecks / Decks |
| 1013 | 13 | Tins? |
| 1014 | 571 | Elite Trainer Boxes / Boxen |
| 1015 | 1.103 | Blister / Checklane |
| 1016 | 170 | Tins / Collections |
| 1017 | 681 | Zubehör (Sleeves, Binder)? |
| 1064 | 28 | ? |
| 1083 | 495 | Sets / Premium Collections? |
| 1654 | 25 | ? |

Die Zuordnung der Nicht-51-Kategorien braucht die Datei `products_nonsingles_6.json` (enthält `categoryName`).

## Datenqualität (Einzelkarten, Kategorie 51)

| Feld | befüllt |
|---|---|
| `low` | 92,2 % |
| `trend` | 88,4 % |
| `avg1`/`avg7`/`avg30` | 84,5 % |
| `avg` | 81,4 % |
| `trend-holo` | 88,3 % |
| `avg7-holo` | 38,9 % |
| `avg-holo` | 26,6 % |

- 4.915 Produkte ohne jeden Preis, 2.773 mit `trend` = 0 → als "kein Preis" behandeln, nicht als 0 €.
- Ausreißer: `low` bis 999.999 €, `avg` bis 100.000 € → `low` ist ein einzelnes Angebot und damit anfällig für Scherzangebote. **Anzeige-Priorität: `trend` > `avg7` > `avg30` > `avg` > `low`.** `low` nur als Zusatzinfo.
- Verteilung `trend` bei Einzelkarten: Median 0,86 €, 90 % unter 23 €, 1 % über 326 €, 179 Karten über 1.000 €.
- Reverse-Holo-Werte (`-holo`) sind spärlicher; Trend fast immer da, Durchschnitte nur bei gut einem Drittel.

## Konsequenzen für das Datenmodell

- `price_snapshots.variant` ∈ {`normal`, `reverse`} direkt aus den zwei Feldgruppen. Holo-Rares (nicht Reverse) laufen bei Cardmarket unter `normal`, weil sie eigenes Produkt sind.
- Sealed-Snapshots bekommen nur `avg`/`low`/`trend`; Charts für Sealed entstehen also ausschließlich aus unserer eigenen Historie.
- Rohdatei täglich archivieren (15 MB, ~5,5 GB/Jahr unkomprimiert, gzip ~1,5 GB) → Storage-Kosten vernachlässigbar.
- Pro Tag ~78k Zeilen × 2 Varianten in `price_snapshots`, ~57 Mio Zeilen/Jahr → Partitionierung nach Monat von Anfang an, `null`-Varianten nicht speichern.

## Offen

1. Nutzungsbedingungen der Data-Seite (Attribution, kommerzielle Nutzung).
2. `products_singles_6.json` prüfen: Enthält `name` Set-Kürzel + Nummer? Gibt es `idExpansion` und ein Expansion-Verzeichnis?
3. Kategorie-Namen aus `products_nonsingles_6.json`.
