# ADR-001: Client-Stack (iOS-App + Desktop-App)

- Status: **Vorgeschlagen** (aktualisiert 2026-09-04 nach neuen Anforderungen)
- Datum: 2026-09-04
- Entscheider: Dev A, Dev B

## Kontext

Anforderungen (Stand 2026-09-04):
- **iOS-App** mit Kamera-Scanner, Offline-Sammlung, Charts, Push, Live Activity / Dynamic Island, Widgets.
- **Desktop-App** (Windows und/oder macOS), mit der Karten über einen **Flachbett- oder Dokumentenscanner** (Drucker-Scanner) in Serie erfasst werden.
- Android ist nicht wichtig.
- Zwei Entwickler in Teilzeit, beide mit Claude Code. Backend in TypeScript (ADR-002).

Der Flachbett-Scanner ist der wichtigste neue Faktor: Ein Browser kann keinen Scanner ansteuern, dafür braucht es eine echte Desktop-App mit Zugriff auf Scanner-Schnittstellen (WIA/TWAIN unter Windows, ImageCaptureCore/SANE unter macOS) oder auf **eSCL/AirScan**, das Netzwerkprotokoll, das fast alle Drucker-Scanner seit ~2018 sprechen und das sich ohne Treiber per HTTP ansteuern lässt.

## Optionen

1. **Expo (React Native) für iOS + Tauri für Desktop, ein TypeScript-Monorepo**
   - Die Expo-App wird zusätzlich als Web-Build kompiliert und läuft in Tauri (leichter Desktop-Wrapper mit Rust-Kern, Windows + macOS + Linux). Ein UI-Code für Handy und Desktop.
   - Scanner: Tauri-Backend spricht eSCL direkt über das Netzwerk (kein Treiber), Fallback über NAPS2-Kommandozeile (Open Source, kann WIA/TWAIN/SANE/eSCL) und als letzte Stufe Ordner-Import ("scanne mit der Herstellersoftware in einen Ordner, wir überwachen ihn").
   - Karten-Matcher (`packages/card-matcher`) ist reines TypeScript und läuft in App, Desktop und Worker identisch.
   - Pro: eine Sprache im gesamten Projekt; Windows-Desktop möglich; Claude Code sehr produktiv in TS; Expo-Ökosystem für Kamera, SQLite, Push.
   - Contra: Live Activity/Widgets brauchen ein kleines Swift-Modul (Expo Modules); Expo-Web für komplexe Screens braucht etwas Sorgfalt; Scanner-Anbindung in Rust oder über Kommandozeilen-Tool ist Neuland für beide.
2. **Native Swift: SwiftUI-App für iOS + macOS aus einer Codebasis**
   - Apple liefert mit ImageCaptureCore eine fertige Scanner-Anbindung für macOS (Flachbett, Dokumenteneinzug, Netzwerk-Scanner). Dynamic Island, Widgets, Vision/CoreML für den Scanner: alles direkt.
   - Pro: beste Qualität auf Apple-Geräten; Scanner-Integration am Mac ist ein Nachmittag statt einer Woche.
   - Contra: **kein Windows-Desktop**; zwei Sprachen im Projekt (Swift + TypeScript-Backend); Matcher-Logik zweimal (Swift für Clients, TS für Worker) oder Worker auch in Swift; erfordert, dass beide Devs Macs haben und Swift lernen wollen.
3. **Expo für iOS + Electron für Desktop**
   - Wie Option 1, aber mit Electron statt Tauri. Scanner-Anbindung über Node-Addons ist möglich, aber altbacken (node-twain, wia-Wrapper) und plattformspezifisch.
   - Contra gegenüber Tauri: 150+ MB Installer, höherer RAM-Verbrauch, kein eingebauter Rust-Kern für eSCL. Kein Vorteil, der das rechtfertigt.
4. **Flutter (iOS + Desktop)**
   - Plattformübergreifend inklusive Windows/macOS-Desktop.
   - Contra: Dart als dritte Sprache; Scanner-Plugins für Desktop sind dünn; iOS-Extras genauso Umweg wie bei Option 1.

## Entscheidungskriterium

**Welches Betriebssystem läuft auf dem Rechner, an dem der Scanner hängt?**
- Windows (oder gemischt) → Option 1.
- Ausschließlich Mac, beide Devs mit Mac, Bereitschaft zu Swift → Option 2 ist ernsthaft attraktiv.

## Empfehlung

Option 1 (Expo + Tauri), solange Windows als Desktop nicht ausgeschlossen ist. Falls beide Devs ausschließlich Apple-Geräte nutzen und Windows nie ein Ziel wird, Option 2 als gleichwertige Alternative gemeinsam abwägen.

## Konsequenzen (bei Option 1)

- Neues Paket `apps/desktop` (Tauri) im Monorepo, das den Web-Build von `apps/mobile` lädt; Scanner-Bridge als Tauri-Command.
- `packages/card-matcher` bekommt zusätzlich eine **Flachbett-Segmentierung** (mehrere Karten auf einer A4-Seite finden, ausschneiden, entzerren ist nicht nötig).
- Roadmap: Desktop-Scanner wird eigenes Arbeitspaket in Phase 2 (siehe `04-roadmap.md`).
- Phase 3 enthält einen Swift-Anteil für Live Activity/Widgets.
