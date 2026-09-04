# CLAUDE.md – PokéVault (Arbeitstitel)

Digitale Pokémon-Kartensammlung mit Preisen, Preis-Historie, Portfolio, Scanner, Grading-Guide. Zwei Entwickler, beide mit Claude Code. Diese Datei gilt für beide; persönliche Vorlieben gehören in `~/.claude/CLAUDE.md`.

## Projektstatus

Planungsphase. Es gibt noch keinen Code. Lies vor jeder Arbeit:
- `docs/03-architecture.md` (Stack, Repo-Struktur, Datenmodell, Scanner-Pipeline)
- `docs/04-roadmap.md` (welche Phase, welche Tasks)
- `docs/05-collaboration.md` (Branching, Ownership, PR-Regeln)
- `docs/adr/` (getroffene Entscheidungen; **Vorgeschlagen** ≠ entschieden)

## Geplanter Stack (siehe ADR-001/002)

- Ziele: iOS-App und macOS-App, pro Nutzer synchron (ADR-004). Android/Windows sind keine Ziele.
- Clients (ADR-001, angenommen): natives Swift. Ein Xcode-Projekt in `apps/apple` mit Targets iOS 17+, macOS 14+ und Widget-Extension; Domänenlogik im Swift-Package `PokeVaultKit` (GRDB, Sync, Matcher, Segmentierung). Kamera über AVFoundation + Vision, Scanner über ImageCaptureCore (ADR-003).
- Backend (ADR-002, angenommen): Supabase in bestehender Org, Region EU, RLS überall. Worker als TypeScript auf Vercel Cron (`apps/worker`). Statische Seiten auf Vercel.
- Monorepo: pnpm workspaces + Turborepo für `apps/worker`, `packages/{shared,db,pricing,card-matcher}`, `supabase/`; Apple-Code daneben in `apps/apple`. Typen aus `packages/shared` werden nach Swift generiert, nie von Hand dupliziert.
- Berechnungen (Preis-Δ, Portfolio-Historie, Winner/Loser, Grading-ROI) leben als Postgres-Views/RPCs, nicht im Client.
- Lokaler Cache im Client (SQLite) + Outbox + Supabase Realtime, Last-Write-Wins über `updated_at`.

## Konventionen

- TypeScript `strict`. Kein `any` ohne Begründungskommentar.
- Geldbeträge: `numeric(12,2)` in DB, in TS als `string`/Decimal, nie `number`-Float. Immer mit Währungsfeld.
- Karten-IDs sind TCGdex-IDs (z. B. `swsh3-136`). Sprache ist Pflichtattribut an jedem Sammlungs-Item.
- Zustände nach Cardmarket-Skala: `MT, NM, EX, GD, LP, PL, PO`. Varianten: `normal, reverse, holo, firstEdition, …` aus `packages/shared`.
- Migrationen: nur über `supabase/migrations/<timestamp>_<name>.sql`, additiv, rückwärtskompatibel. Jede Nutzertabelle bekommt RLS (`user_id = auth.uid()`).
- Contract-first: Typen/Zod-Schemas, die App und Worker teilen, zuerst in `packages/shared` als eigener kleiner PR.
- Reine TS-Logik (Index-Bau, Preis-Jobs) lebt in `packages/*` mit Vitest-Tests; Swift-Logik in `PokeVaultKit` mit XCTest. Der Hash-Algorithmus existiert in beiden Sprachen und muss `fixtures/hash-vectors.json` bestehen.
- Commits: Conventional Commits mit Paket-Scope (`feat(worker): daily price snapshot job`). Kleine PRs (< 400 Zeilen). Squash-Merge auf `main`.
- Keine Secrets im Repo. `.env.example` pflegen.

## Swift-Konventionen

- SwiftUI, Swift Concurrency (`async/await`), kein Combine für neue Logik.
- Keine Force-Unwraps (`!`) außerhalb von Tests. Fehler als typisierte `Error`-Enums.
- Plattform-Code nur hinter `#if os(macOS)` / `#if os(iOS)` in eigenen Dateien, nicht in geteilten Views verstreut.
- Geld als `Decimal`, nie `Double`.

## Verboten

- Scraping von cardmarket.com, ebay.com oder anderen Marktplätzen. Erlaubt sind nur die offiziellen Cardmarket-Download-Dateien (Price Guide, Produktkatalog).
- Offizielle Pokémon-Logos/Wordmarks/Artworks als App-Assets (Kartenbilder kommen von TCGdex per URL).
- `git push --force` auf `main` oder auf Branches anderer.
- Migrationen mit Sequenznummern statt Timestamp.
- Test-Skips oder Quarantäne, um CI grün zu bekommen.

## Befehle (sobald das Monorepo steht)

```
pnpm i                 # Install
pnpm dev               # Worker lokal (vercel dev)
open apps/apple/PokeVault.xcodeproj   # Clients in Xcode
pnpm lint && pnpm typecheck && pnpm test
supabase start         # lokale Supabase
pnpm db:migrate        # Migrationen anwenden
```

## Arbeitsweise mit Claude Code

- Für alles über eine Datei: Plan-Modus zuerst, Plan kurz abstimmen, dann umsetzen.
- Issue-Nummer im Prompt nennen ("Implementiere #42"); Akzeptanzkriterien aus dem Issue sind die Definition of Done.
- Wenn du eine Architekturentscheidung triffst, die nicht in `docs/adr/` steht: ADR anlegen (Vorlage `docs/adr/000-template.md`) statt still zu entscheiden.
- Eigene Branch/Worktree pro Aufgabe; nie in der Working Copy des anderen arbeiten.
