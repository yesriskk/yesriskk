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
- Clients: ADR-001 offen zwischen nativem Swift (empfohlen; ein Xcode-Projekt, `apps/apple`, Domänen-Package `PokeVaultKit`) und Expo + Tauri. Bis zur Entscheidung keinen Client-Code anlegen.
- Backend (ADR-002, angenommen): Supabase in bestehender Org, Region EU, RLS überall. Worker als TypeScript auf Vercel Cron (`apps/worker`). Statische Seiten auf Vercel.
- Monorepo: pnpm workspaces + Turborepo für `apps/worker`, `packages/{shared,db,pricing,card-matcher}`, `supabase/`; Apple-Code daneben in `apps/apple`.
- Lokaler Cache im Client (SQLite) + Outbox + Supabase Realtime, Last-Write-Wins über `updated_at`.

## Konventionen

- TypeScript `strict`. Kein `any` ohne Begründungskommentar.
- Geldbeträge: `numeric(12,2)` in DB, in TS als `string`/Decimal, nie `number`-Float. Immer mit Währungsfeld.
- Karten-IDs sind TCGdex-IDs (z. B. `swsh3-136`). Sprache ist Pflichtattribut an jedem Sammlungs-Item.
- Zustände nach Cardmarket-Skala: `MT, NM, EX, GD, LP, PL, PO`. Varianten: `normal, reverse, holo, firstEdition, …` aus `packages/shared`.
- Migrationen: nur über `supabase/migrations/<timestamp>_<name>.sql`, additiv, rückwärtskompatibel. Jede Nutzertabelle bekommt RLS (`user_id = auth.uid()`).
- Contract-first: Typen/Zod-Schemas, die App und Worker teilen, zuerst in `packages/shared` als eigener kleiner PR.
- Reine Logik (Matcher, Preis-Δ, P&L) lebt in `packages/*` ohne React-Native-Imports und hat Vitest-Tests.
- Commits: Conventional Commits mit Paket-Scope (`feat(worker): daily price snapshot job`). Kleine PRs (< 400 Zeilen). Squash-Merge auf `main`.
- Keine Secrets im Repo. `.env.example` pflegen.

## Verboten

- Scraping von cardmarket.com, ebay.com oder anderen Marktplätzen. Erlaubt sind nur die offiziellen Cardmarket-Download-Dateien (Price Guide, Produktkatalog).
- Offizielle Pokémon-Logos/Wordmarks/Artworks als App-Assets (Kartenbilder kommen von TCGdex per URL).
- `git push --force` auf `main` oder auf Branches anderer.
- Migrationen mit Sequenznummern statt Timestamp.
- Test-Skips oder Quarantäne, um CI grün zu bekommen.

## Befehle (sobald das Monorepo steht)

```
pnpm i                 # Install
pnpm dev               # Expo + Worker lokal
pnpm lint && pnpm typecheck && pnpm test
supabase start         # lokale Supabase
pnpm db:migrate        # Migrationen anwenden
```

## Arbeitsweise mit Claude Code

- Für alles über eine Datei: Plan-Modus zuerst, Plan kurz abstimmen, dann umsetzen.
- Issue-Nummer im Prompt nennen ("Implementiere #42"); Akzeptanzkriterien aus dem Issue sind die Definition of Done.
- Wenn du eine Architekturentscheidung triffst, die nicht in `docs/adr/` steht: ADR anlegen (Vorlage `docs/adr/000-template.md`) statt still zu entscheiden.
- Eigene Branch/Worktree pro Aufgabe; nie in der Working Copy des anderen arbeiten.
