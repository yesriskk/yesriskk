# 05 – Zusammenarbeit zu zweit mit Claude Code

Ziel: Beide arbeiten gleichzeitig, ohne sich gegenseitig zu blockieren oder Merge-Konflikte zu produzieren. Beide nutzen Claude Code, also müssen die Konventionen **maschinenlesbar** im Repo liegen, nicht in Chats.

## 1. Das Repo ist die Wahrheit

- `CLAUDE.md` im Root: Stack, Konventionen, Befehle, Verbote. Wird von Claude Code bei beiden automatisch geladen. Persönliche Vorlieben gehören in `~/.claude/CLAUDE.md`, nicht ins Repo.
- `.claude/settings.json` (committed): geteilte Permissions (z. B. `pnpm test` erlaubt) und Hooks (Lint/Format nach Edit). `.claude/settings.local.json` ist gitignored.
- `.claude/commands/`: wiederkehrende Prompts als Slash-Commands (`/new-migration`, `/new-screen`, `/review-pr`), damit beide Devs und beide Claudes dieselben Muster erzeugen.
- `docs/adr/`: Jede Architekturentscheidung als kurzes ADR. Claude Code liest die ADRs, wenn sie in `CLAUDE.md` referenziert sind → weniger "Claude hat's anders gebaut".

## 2. Paketgrenzen = Konfliktgrenzen

Das Monorepo ist so geschnitten, dass paralleles Arbeiten selten dieselben Dateien berührt:

| Paket | Typischer Owner | Regel |
|---|---|---|
| `apps/mobile` | Dev A | Screens, Navigation, Kamera |
| `apps/worker` | Dev B | Cron, Provider-Orchestrierung, HTTP-Endpoints |
| `packages/db` | Dev B | Migrationen **nur** über `/new-migration` (Timestamp-Prefix, nie Sequenznummern → keine Kollisionen) |
| `packages/shared` | gemeinsam | **Contract-first**: Wer ein Feature braucht, das beide Seiten berührt, legt zuerst Zod-Schema/Typ in `shared` an und merged das als eigenen kleinen PR. Danach arbeiten beide gegen den Typ. |
| `packages/card-matcher`, `packages/pricing` | Dev B (Logik), Dev A (Integration) | reine TS-Pakete mit Unit-Tests, keine RN-Imports |
| `packages/ui` | Dev A | Komponenten; Dev B nutzt, ändert nur per PR mit Review |

Ownership heißt "erster Reviewer", nicht "nur der darf". Vertikale Features (z. B. Wishlist = Schema + Worker-Alarm + Screen) werden bewusst aufgeteilt: Contract-PR → zwei parallele PRs.

## 3. Git-Workflow

- **Trunk-based**: `main` ist immer deploybar. Feature-Branches leben < 3 Tage.
- Branch-Namen: `feat/<kurz>`, `fix/<kurz>`, `chore/<kurz>`, `docs/<kurz>`. Claude-Code-Branches (`claude/...`) sind ok, werden aber vor dem PR umbenannt oder als solche gelabelt.
- **Conventional Commits** (`feat(mobile): scanner review queue`). Scope = Paketname.
- **PR-Pflicht** mit CI grün + 1 Review. Squash-Merge. Kleine PRs (< 400 Zeilen Diff) sind das Ziel; Claude Code neigt zu großen Diffs, also bewusst splitten.
- Reviewer nutzt `/code-review` in Claude Code als Vor-Review, entscheidet aber selbst.
- Nie `git push --force` auf `main` oder auf Branches des anderen.
- Jeder arbeitet in eigenem Clone oder **git worktree** pro Branch, damit parallele Claude-Sessions sich nicht die Working Copy zerschießen.

## 4. Arbeitsrhythmus

- **Issue zuerst, dann Code.** Jedes Feature ist ein GitHub Issue mit Akzeptanzkriterien. Claude Code bekommt das Issue als Prompt-Kontext ("Implementiere #42").
- Claude Code im **Plan-Modus** starten für alles über 1 Datei, Plan kurz gegenlesen, dann bauen.
- **Wöchentliches 30-Minuten-Sync** (Call oder Voice): Board durchgehen, nächste Issues zuweisen, Konfliktpotenzial ansprechen.
- Asynchron: GitHub-Diskussionen in Issues/PRs, nicht in Chat-Apps, damit Claude den Kontext später findet.

## 5. Qualität, die beide Claudes einhalten müssen

- TypeScript `strict`, kein `any` ohne Kommentar.
- Jede reine Logik (Matcher, Preis-Berechnung, P&L) hat Unit-Tests (Vitest). UI-Logik in Hooks, testbar.
- Migrationen sind additiv und rückwärtskompatibel innerhalb einer Phase (App-Versionen im Feld!).
- Keine Secrets im Repo; `.env.example` pflegen.
- Definition of Done: CI grün, auf echtem Gerät getestet, Issue-Akzeptanzkriterien abgehakt, Doku/ADR aktualisiert falls betroffen.

## 6. Umgebungen

| Umgebung | Zweck | Wer |
|---|---|---|
| Lokal (`supabase start`, Worker lokal) | Entwicklung | jeder |
| `staging` Supabase-Projekt + Worker | Preview-Builds, gemeinsames Testen | geteilt |
| `prod` | TestFlight/Store | nur über `main` |

Preis-Snapshots laufen ab Phase 0 **nur in prod**, Staging bekommt eine wöchentliche Kopie (Historie nicht verlieren).

## 7. Onboarding des Freundes (Checkliste)

1. Repo klonen, `pnpm i`, `supabase start`, `pnpm dev`.
2. `CLAUDE.md`, `docs/00`–`06` lesen, ADRs überfliegen.
3. Claude Code im Repo öffnen, `/init` **nicht** ausführen (CLAUDE.md existiert schon), stattdessen `/new-screen`-Command ausprobieren.
4. Ersten kleinen Issue (`good first issue`) per PR abschließen, um den Workflow zu testen.
