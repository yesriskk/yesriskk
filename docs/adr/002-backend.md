# ADR-002: Backend

- Status: **Angenommen** (2026-09-04)
- Datum: 2026-09-04
- Entscheider: Dev A, Dev B

## Kontext

Auth, relationale DB mit Zeitreihen (Preis-Snapshots), Object Storage für Fotos, Push, tägliche Batch-Jobs, Realtime-Sync zwischen iPhone und Mac. EU-Hosting. Vorhanden: eine Supabase-Organisation (Pro) aus einem anderen Projekt und Vercel Pro.

## Entscheidung

1. **Supabase**, neues Projekt in der bestehenden Organisation, Region **EU (Frankfurt)**: Postgres, Auth (E-Mail + Sign in with Apple), Storage (Nutzerfotos), Realtime (Sync-Signal), RLS auf allen Nutzertabellen. Getrennt vom anderen Projekt, keine geteilte Datenbank.
2. **Worker auf Vercel** (Pro-Plan vorhanden): Vercel Cron Jobs stoßen serverlose Funktionen an (TypeScript, Hono oder Next.js Route Handlers). Pro erlaubt beliebig viele Crons und bis zu 300 s Laufzeit pro Funktion (mit Fluid Compute bis 800 s). Der tägliche Cardmarket-Lauf (15 MB laden, 78k Zeilen upserten) wird in Chunks à ~10k Zeilen aufgeteilt, damit er sicher im Limit bleibt; Katalog-Import (einmalig, groß) läuft lokal per Skript.
3. Statische Seiten (Datenschutz, Impressum, Landingpage, später Web-Ansicht der Sammlung) ebenfalls auf Vercel.

Verworfen: eigener Server (Betriebsaufwand), Firebase (Zeitreihen und Aggregate unhandlich), Fly.io/Railway für den Worker (unnötig, da Vercel Pro vorhanden; bleibt Fallback, falls Laufzeitlimits stören).

## Konsequenzen

- Clients sprechen CRUD direkt mit Supabase (PostgREST + RLS); Worker nutzt den Service-Role-Key ausschließlich serverseitig in Vercel-Env-Vars.
- Migrationen als SQL in `supabase/migrations` (Timestamp-Prefix), lokal mit `supabase start`, Deploy über `supabase db push` in CI.
- Ein Vercel-Projekt `apps/worker` mit `vercel.json`-Crons; Alerting über Vercel-Log-Drains oder einfachen Healthcheck (z. B. Better Stack / Cronitor, Free-Tier).
- Kostenerwartung: Supabase-Projekt im Pro-Org ~25 USD/Monat (falls nicht vom Free-Kontingent gedeckt), Vercel ohne Mehrkosten.
