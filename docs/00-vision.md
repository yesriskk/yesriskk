# 00 – Vision

## Ein Satz

**Die App, mit der Sammler ihre Pokémon-Karten in Sekunden erfassen, den Wert ihrer Sammlung jederzeit kennen und bessere Kauf-, Verkaufs- und Grading-Entscheidungen treffen.**

## Zielgruppe

| Persona | Was sie will | Kernfeatures |
|---|---|---|
| **Sammler** (Master-Sets, Binder) | Übersicht, was fehlt, was doppelt ist, Bilder in der eigenen Sprache | Scanner, Master-Set-Tracker, Binder, Wishlist |
| **Investor** | Wertentwicklung, Winner/Loser, Sealed-Produkte, Ein-/Ausstiegs-Signale | Portfolio, Preis-Charts, Alarme, Investment-Tracking |
| **Grader/Flipper** | Welche Karte lohnt sich zum Graden, wo einreichen, was kostet es | Grading-Guide, ROI-Rechner, Pregrading-Check, Graded-Preise |
| **Verkäufer** | Schnell listen, Preise kennen, Verkäufe tracken | eBay-Listing, Verkaufsverlauf, Realized P&L |

Primärmarkt: **DACH / Europa** (EUR, Cardmarket als Referenz, deutsche Karten). Sekundär: EN-Markt (USD, TCGplayer).

## Nicht-Ziele (bewusst außerhalb des Scopes, mindestens bis v2)

- Deck-Builder / Spielfunktionen (wir bauen für Sammler, nicht für Spieler).
- Eigener Marktplatz mit Zahlungsabwicklung.
- Andere TCGs (Magic, One Piece, Lorcana). Das Datenmodell soll es aber nicht verhindern (`game`-Spalte von Anfang an).
- Android-Parität für rein iOS-spezifische Features (Dynamic Island, Live Activities).

## Erfolgskriterien für v1.0

- Eine 500-Karten-Sammlung lässt sich in unter 30 Minuten per Scanner erfassen (Trefferquote ≥ 95 % bei guter Beleuchtung).
- Preise für ≥ 95 % der Karten seit Sword & Shield vorhanden, täglich aktualisiert.
- Portfolio-Wert und 30-Tage-Entwicklung auf einen Blick.
- Beide Entwickler können unabhängig voneinander Features shippen, ohne sich zu blockieren.

## Leitprinzipien

1. **Offline-first**: Sammlung ist lokal immer verfügbar, Sync passiert im Hintergrund.
2. **Eigene Preis-Historie**: Wir speichern täglich Snapshots und sind damit nicht von einer externen Historien-API abhängig.
3. **Sprache ist ein First-Class-Attribut**: Jede Karte hat eine Sprache, jedes Bild kommt in der passenden Sprache.
4. **Erst Daten, dann Glanz**: Katalog + Preise + Portfolio stabil, bevor Scanner-Magie und Dynamic Island kommen.
5. **Legal sauber**: Keine Scraper gegen Cardmarket/eBay, keine offiziellen Pokémon-Logos, Datenquellen mit klaren Nutzungsbedingungen.
