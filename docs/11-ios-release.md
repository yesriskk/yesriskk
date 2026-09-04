# 11 – iOS-Release: Voraussetzungen und Kosten

Stand 2026-09-04. Preise sind Richtwerte, bitte vor Kauf auf den Apple-Seiten prüfen.

## Entwickeln und testen ohne Developer Program

Ja, das geht, und zwar recht weit:

| Was | Ohne Developer Program (kostenlose Apple-ID) | Braucht das Programm (99 USD/Jahr) |
|---|---|---|
| iOS-Simulator in Xcode | ✅ voll, inklusive Dynamic-Island-Simulator (iPhone 15 Pro und neuer) und Live Activities | |
| macOS-App lokal starten | ✅ | |
| App auf dem **eigenen** iPhone per Kabel | ✅ "Personal Team": App läuft 7 Tage, dann neu installieren; max. 3 Apps gleichzeitig | |
| Kamera-Scanner testen | ✅ nur auf echtem iPhone (Simulator hat keine Kamera) | |
| Flachbett-Scanner am Mac testen | ✅ | |
| Supabase-Login mit E-Mail/Passwort | ✅ | |
| Push-Notifications | ❌ | ✅ |
| Sign in with Apple | ❌ | ✅ |
| Live Activity auf echtem Gerät | ✅ (Personal Team erlaubt es meist), Push-Updates dafür ❌ | ✅ |
| App an den Freund geben (TestFlight) | ❌ (nur per Kabel auf sein Gerät mit seiner eigenen Apple-ID) | ✅ |
| Xcode Cloud, App Store, notarisierter Mac-Download | ❌ | ✅ |

**Empfehlung:** Phase 0 und der Großteil von Phase 1 laufen ohne Programm. Abschließen, sobald ihr Push-Notifications baut oder euch gegenseitig Builds per TestFlight schicken wollt, realistisch Ende Phase 1.

## Was ihr braucht

| Punkt | Details | Kosten |
|---|---|---|
| **Apple Developer Program** | Pflicht für TestFlight und App Store. Ein Account (Einzelperson oder Organisation) hält die App; der zweite Entwickler wird in App Store Connect als Nutzer eingeladen. Für Organisation braucht es eine D-U-N-S-Nummer (kostenlos, dauert Tage); als Einzelperson reicht Apple-ID + Ausweis. | **99 USD/Jahr** (in DE ca. 99 €/Jahr) |
| **Mac mit Xcode** | Vorhanden bei beiden. Xcode ist kostenlos. | 0 € |
| **Xcode Cloud** | Baut, testet und lädt zu TestFlight hoch; 25 Stunden/Monat sind im Developer Program enthalten. Alternativ Fastlane lokal. | im Programm enthalten |
| **iPhone zum Testen** | Kamera, Push, Live Activity lassen sich nicht im Simulator testen. Dynamic Island braucht iPhone 14 Pro oder neuer. | vorhanden |
| **Datenschutzerklärung + Impressum** | Als URL Pflicht im App-Store-Eintrag (Deutschland: Impressumspflicht). Generator + eigene Domain. | Domain ~10 €/Jahr |
| **App-Privacy-Angaben** | Formular in App Store Connect: welche Daten (E-Mail, Fotos, Nutzungsdaten) und wofür. Muss zur App passen. | 0 € |
| **Sign in with Apple** | Pflicht, sobald ihr einen anderen Drittanbieter-Login (Google, etc.) anbietet. Supabase Auth unterstützt Apple. E-Mail/Passwort allein braucht es nicht. | 0 € |
| **Export-Compliance** | Frage zur Verschlüsselung beim Upload; bei reinem HTTPS "exempt" ankreuzen. | 0 € |
| **In-App-Kauf** | Ein Pro-Abo **muss** über Apple In-App Purchase laufen (kein externer Bezahllink für digitale Features). Provision 30 %, mit **Small Business Program** (unter 1 Mio USD Umsatz/Jahr) 15 %. Umsetzung über StoreKit 2 oder RevenueCat. | 15 % vom Umsatz |
| **Markenrecht** | Kein "Pokémon" im App-Namen, kein offizielles Logo im Icon oder in Screenshots. Apple prüft Guideline 5.2 (Intellectual Property) aktiv; Ablehnungen sind bei Pokémon-Apps häufig. Disclaimer im Store-Text. | 0 €, aber Release-Risiko |
| **Review-Zeit** | Erste Einreichung 1–3 Tage, Updates meist < 24 h. Ablehnungen kosten je eine Runde. | – |

## Ablauf bis zum ersten TestFlight (Phase 1)

1. Apple Developer Program abschließen (Freischaltung dauert 1–2 Tage).
2. Bundle-IDs festlegen (z. B. `de.<euredomain>.pokevault` für iOS und macOS, `.widgets` für die Extension).
3. In Xcode "Automatically manage signing" mit dem Team-Account aktivieren; Xcode erstellt Zertifikate und Profile.
4. Archive → Distribute → TestFlight (oder Xcode Cloud Workflow); interne Tester (bis 100) sofort, externe Tester (bis 10.000) nach kurzem Beta-Review.
5. Für Push: APNs-Key im Developer-Portal erzeugen und in Supabase/Worker hinterlegen.

## Ablauf bis zum App-Store-Release (Phase 4)

1. App-Store-Eintrag: Name, Untertitel, Beschreibung, Keywords, Screenshots (6,7" und 6,1" Pflicht), Icon 1024 px, Alterseinstufung, Kategorie.
2. Datenschutz-URL, Support-URL, App-Privacy-Formular.
3. Review-Notizen mit Test-Account, falls Login nötig.
4. Falls Abo: Produkte in App Store Connect anlegen, Preisstufen, Abo-Gruppe; Sandbox-Test.
5. Einreichen, auf Review reagieren, Release manuell oder automatisch.

## Desktop-Verteilung (zum Vergleich)

| Plattform | Weg | Kosten |
|---|---|---|
| macOS | Direkter Download: Notarisierung über dasselbe Developer Program (Pflicht, sonst Gatekeeper-Warnung). Mac App Store optional. | im 99-USD-Programm enthalten |
| Windows | Direkter Download oder Microsoft Store. Ohne Code-Signing zeigt SmartScreen eine Warnung; ein Zertifikat kostet ca. 200–400 €/Jahr, kann anfangs entfallen. | 0 € bis ~300 €/Jahr |

## Laufende Kosten gesamt (Schätzung erstes Jahr)

| Posten | Betrag |
|---|---|
| Apple Developer Program | ~99 €/Jahr |
| Supabase (Pro-Plan sobald nötig) | 0–25 USD/Monat |
| Worker-Hosting (Fly.io/Railway) | 0–5 USD/Monat |
| Xcode Cloud | im Programm enthalten |
| Domain | ~10 €/Jahr |
| Graded-Preise (optional, ab Phase 3) | 29–99 USD/Monat |
| **Summe ohne Graded-Preise** | **~100–700 € im ersten Jahr**, je nach Nutzung der Free-Tiers |
