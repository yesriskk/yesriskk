# ADR-002: Backend

- Status: **Vorgeschlagen**
- Datum: 2026-09-04
- Entscheider: Dev A, Dev B

## Kontext

Wir brauchen Auth, eine relationale DB mit Zeitreihen-Charakter (Preis-Snapshots), Object Storage für Fotos, Push und tägliche Batch-Jobs. EU-Hosting wegen DSGVO. Kleines Team, wenig Ops-Zeit.

## Optionen

1. **Supabase (Postgres, Auth, Storage, RLS) + separater Node-Worker** für Jobs.
2. Eigenes Postgres + Node-API (Hono/Fastify) + eigenes Auth.
3. Firebase/Firestore.

## Entscheidung (Vorschlag)

Option 1. Supabase nimmt uns Auth, Storage, RLS und Realtime ab; Postgres passt zu Zeitreihen (Partitionierung) und Auswertungen (Views, Window-Functions). Der Worker läuft als eigener Container (Fly.io/Railway, EU), weil Edge Functions für 20k-Karten-Batches zu limitiert sind.

Firestore verworfen: Aggregationen und Zeitreihen sind dort unhandlich und teuer.

## Konsequenzen

- Client spricht CRUD direkt mit Supabase (RLS ist Pflicht für jede Nutzertabelle).
- Alles, was Secrets braucht (eBay, Bezahl-APIs), läuft ausschließlich im Worker.
- Lokale Entwicklung über `supabase start`; Migrationen als SQL in `supabase/migrations` mit Timestamp-Prefix, Drizzle-Schema in `packages/db` als typisierte Spiegelung.
