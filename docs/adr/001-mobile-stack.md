# ADR-001: Mobile-Stack

- Status: **Vorgeschlagen** (muss von beiden bestätigt werden)
- Datum: 2026-09-04
- Entscheider: Dev A, Dev B

## Kontext

Wir brauchen eine Kamera-App mit Echtzeit-Bildverarbeitung (Scanner), Offline-Datenhaltung, Charts, Push und iOS-spezifischen Features (Live Activity / Dynamic Island, Widgets). Zwei Entwickler, beide mit Claude Code. Primär iOS, Android erwünscht.

## Optionen

1. **Expo (React Native) + TypeScript**
   - Pro: iOS + Android; TypeScript im gesamten Stack (App, Worker, Shared-Pakete); sehr gute Claude-Code-Produktivität; `react-native-vision-camera` mit Frame-Prozessoren für Echtzeit-Scanning; EAS für Builds; große Ökosystem-Abdeckung (Charts, SQLite, Push).
   - Contra: Live Activities/Widgets brauchen Swift-Code via Expo Modules; Frame-Prozessoren mit Bildverarbeitung brauchen ggf. ein natives Modul (OpenCV/Vision); zusätzliche Abstraktionsschicht bei nativen Bugs.
2. **Native SwiftUI**
   - Pro: Vision/CoreML/ActivityKit/WidgetKit direkt; beste Kamera-Performance; Dynamic Island ohne Umweg.
   - Contra: iOS-only; zwei Sprachen im Projekt (Swift + TS-Backend); geteilte Typen/Validierung müssen dupliziert werden.
3. **Flutter**
   - Pro: Cross-Platform, gute Performance, ML Kit Plugins.
   - Contra: Dart als dritte Sprache neben TS-Backend; iOS-Extension-Integration ähnlich aufwendig wie bei RN; kleineres TCG-/Community-Ökosystem.

## Entscheidung (Vorschlag)

Option 1, Expo + TypeScript, mit einem klar abgegrenzten Swift-Paket (`apps/mobile/modules/ios-native`) für Live Activity, Widgets und alternative Icons.

Wechsel zu Option 2, falls beide Devs beschließen, Android bewusst aufzugeben **und** mindestens einer sicher in Swift ist.

## Konsequenzen

- Ein Sprach-Stack, ein Lint/Test-Setup, geteilte Zod-Schemas.
- Scanner-Kern (`packages/card-matcher`) bleibt reines TS und ist in Node testbar.
- Phase 3 enthält einen Swift-Anteil; Zeit dafür einplanen (Expo Config Plugin, Xcode-Target).
