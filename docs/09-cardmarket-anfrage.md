# 09 – Anfrage an Cardmarket (Entwurf)

Ziel: schriftliche Zustimmung, die öffentlich herunterladbaren Price-Guide- und Produktkatalog-Dateien in unserer Sammler-App anzuzeigen. Vor dem Absenden: App-Name einsetzen, Data-Seite auf eigene Bedingungen prüfen, Kontaktweg wählen (Helpdesk-Ticket über help.cardmarket.com oder, falls vorhanden, Partner-/Business-Kontakt).

---

**Betreff:** Nutzung der öffentlichen Price-Guide-Downloads in einer Pokémon-Sammler-App

Hallo Cardmarket-Team,

wir entwickeln eine mobile App (Arbeitstitel: PokéVault) für Pokémon-Sammler, mit der Nutzer ihre Sammlung digital erfassen und den Wert ihrer Karten verfolgen können. Wir sind zwei Entwickler aus Deutschland und befinden uns in der Planungsphase.

Wir möchten dafür die von Cardmarket öffentlich bereitgestellten Dateien nutzen, die unter cardmarket.com/de/Pokemon/Data/Price-Guide zum Download angeboten werden (täglicher Price Guide sowie Produktkatalog für Singles und Non-Singles).

Konkret planen wir:

1. Die Dateien einmal täglich herunterzuladen und die Werte (Trend, Durchschnitt, 1/7/30-Tage-Durchschnitt) je Produkt in unserer Datenbank zu speichern, um daraus eine Preishistorie aufzubauen.
2. Diese Werte in der App bei der jeweiligen Karte als "Cardmarket-Preis" anzuzeigen, mit sichtbarer Quellenangabe und Link zur Produktseite auf cardmarket.com.
3. Aggregierte Werte (Sammlungswert, Wertentwicklung, Preisalarme) daraus zu berechnen.

Wir planen ausdrücklich **nicht**: Scraping der Website, Anzeige einzelner Angebote oder Verkäufer, Weitergabe der Rohdaten an Dritte oder Anbieten der Daten als eigene API.

Die App soll kostenlos nutzbar sein, mit optionalen kostenpflichtigen Zusatzfunktionen (z. B. erweiterte Statistiken). Wir sehen die App als Ergänzung zu Cardmarket: Nutzer sehen bei jeder Karte den Cardmarket-Preis und können direkt zum Kauf oder zur Angebotserstellung auf Cardmarket wechseln.

Ihre AGB nennen im Abschnitt zur API, dass die Darstellung von Karten und Preisen eine vorherige schriftliche Zustimmung erfordert. Da die Download-Dateien die früheren API-Endpunkte ersetzen, möchten wir sichergehen und bitten um Ihre schriftliche Zustimmung zur oben beschriebenen Nutzung, beziehungsweise um Hinweise, unter welchen Bedingungen (Attribution, Linkpflicht, Aktualisierungsintervall, Umfang) eine Nutzung für Sie in Ordnung ist.

Gerne stellen wir weitere Informationen bereit oder sprechen kurz telefonisch.

Vielen Dank und freundliche Grüße
[Name], [Name]
[Kontakt]

---

## Nach der Antwort

- Antwort im Wortlaut in `02-data-sources.md` Abschnitt 8a ablegen, Datum und Ansprechpartner notieren.
- Bei Bedingungen (Attribution, Linkpflicht): als Akzeptanzkriterien in die betroffenen Issues (Kartendetail, Portfolio) übernehmen.
- Bei Ablehnung: ADR anlegen, Preis-Provider auf TCGdex/Bezahl-API umstellen, Risiko in `06` aktualisieren.
