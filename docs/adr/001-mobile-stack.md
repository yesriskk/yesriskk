# ADR-001: Client-Stack (iOS-App + macOS-App)

- Status: **Vorgeschlagen, Entscheidung steht an** (aktualisiert 2026-09-04)
- Datum: 2026-09-04
- Entscheider: Dev A, Dev B

## Kontext

Festgelegt am 2026-09-04:
- Ziele sind **iOS-App** und **macOS-App**. Android und Windows sind keine Ziele.
- Die macOS-App erfasst Karten über einen **Flachbett-/Dokumentenscanner**; die iOS-App per Kamera.
- Beide Clients sind über einen gemeinsamen Nutzer-Account **synchron**: Was am Mac gescannt wird, erscheint auf dem iPhone und umgekehrt (ADR-004).
- Backend: bestehende Supabase-Organisation, Jobs auf Vercel Pro (ADR-002).
- Zwei Entwickler in Teilzeit, beide mit Claude Code.

Mit dem Wegfall von Windows und Android fällt das stärkste Argument für React Native weg. Übrig bleibt die Frage: **eine Sprache im Projekt (TypeScript überall) oder die beste Apple-Integration (Swift für die Clients)?**

## Optionen

### Option A: Native Swift, ein Xcode-Projekt mit iOS- und macOS-Target (SwiftUI)

- Ein SwiftUI-Code für beide Plattformen; plattformspezifische Views nur dort, wo nötig (Scanner-Fenster am Mac, Kamera am iPhone).
- **Scanner:** Apples `ImageCaptureCore` spricht Flachbett-, Einzugs- und Netzwerkscanner direkt, ohne Treiber, ohne Zusatzsoftware. Die Scanner-Anbindung ist damit ein Nachmittag statt einer Woche.
- **Kamera:** `AVFoundation` + `Vision` (Rechteck-Erkennung, OCR) sind eingebaut und schnell.
- **Dynamic Island / Live Activity / Widgets:** direkt mit ActivityKit und WidgetKit, kein Brückenmodul.
- **Sync:** offizielles `supabase-swift` SDK (Auth, Datenbank, Realtime, Storage). Lokaler Cache mit GRDB (SQLite) oder SwiftData.
- Pro: beste Qualität und Performance auf beiden Zielplattformen; jede Anforderung (Scanner, Kamera, Island) ist ein First-Class-Apple-Feature; kein Webview am Mac; Claude Code ist in Swift/SwiftUI produktiv.
- Contra: zwei Sprachen im Projekt (Swift-Clients, TypeScript-Backend); Domänenlogik wie Preis-Δ oder P&L existiert zweimal, oder das Backend liefert fertige Werte; der Karten-Matcher (Hashing) muss in Swift laufen und im Worker in TypeScript zum Index-Bau, mit gemeinsamen Testvektoren; beide Devs brauchen Xcode und Bereitschaft zu Swift.

### Option B: Expo (React Native) für iOS + Tauri für macOS, alles TypeScript

- Ein Code für iPhone und Mac (Expo-Web-Build im Tauri-Webview).
- Scanner über eSCL/AirScan im Netzwerk (Rust in Tauri) oder Ordner-Import; `ImageCaptureCore` wäre nur über ein zusätzliches Swift-Hilfsprogramm erreichbar.
- Live Activity/Widgets über ein Swift-Expo-Modul.
- Pro: eine Sprache; geteilte Typen und Logik ohne Duplikate; Web-Version quasi gratis.
- Contra: die Mac-App ist ein Webview, kein natives Fenster; drei Brücken (eSCL-Scanner, Swift-Widgets, Kamera-Frame-Prozessor) statt null; USB-only-Scanner brauchen Zusatzsoftware.

### Option C: Flutter

Keine Vorteile gegenüber A oder B in einem reinen Apple-Setup. Verworfen.

## Empfehlung

**Option A (native Swift)**, unter einer Bedingung: Beide Entwickler haben einen Mac und wollen die Clients in Swift schreiben. Begründung: Alle drei anspruchsvollen Anforderungen (Flachbett-Scanner, Kamera-Erkennung, Dynamic Island) sind unter Swift eingebaute Plattformfunktionen und unter Option B jeweils eine Brücke mit eigenem Risiko. Bei zwei Personen in Teilzeit zählt, wie viele Baustellen gleichzeitig offen sind.

Falls einer von beiden Swift ablehnt, ist Option B tragfähig und wird mit ADR-003 (eSCL) umgesetzt.

## Konsequenzen bei Option A

- Repo-Struktur: `apps/apple/` (Xcode-Projekt, Swift Package für Domänenlogik `PokeVaultKit`), `apps/worker/` (TypeScript auf Vercel), `packages/shared/` (Zod-Schemas + **generierte Swift-Typen** aus derselben Quelle, z. B. über OpenAPI/JSON-Schema → Swift Codegen), `supabase/`.
- Matcher: Hash-Algorithmus (dHash/pHash) in Swift **und** TypeScript, mit gemeinsamen Fixtures (`fixtures/hash-vectors.json`), die beide Implementierungen bestehen müssen.
- Berechnete Werte (Preis-Δ, Portfolio-Historie, Winner/Loser, Grading-ROI) liefert das Backend als Views/RPCs, damit die Logik nur einmal existiert. Der Client rechnet nur, was offline nötig ist (Summen).
- CI: GitHub Actions mit macOS-Runner für Xcode-Build und Tests (teurer als Linux-Runner, ~10× Minutenpreis; Budget beachten oder Xcode Cloud nutzen, 25 h/Monat im Developer Program enthalten).
- Kein EAS nötig; Builds und TestFlight über Xcode Cloud oder Fastlane.
