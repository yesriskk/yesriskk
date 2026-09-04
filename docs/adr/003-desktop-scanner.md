# ADR-003: Desktop-Scanner-Anbindung (Flachbett)

- Status: **Vorgeschlagen**
- Datum: 2026-09-04
- Entscheider: Dev A, Dev B

## Kontext

Karten sollen am Desktop über einen Flachbett- oder Dokumentenscanner erfasst werden. Auf eine A4-Fläche passen 9 Karten (3×3 bei 63×88 mm), auf A3 rund 20. Ein Scan bei 300 dpi dauert je nach Gerät 10–25 s. Der Scan liefert im Gegensatz zur Handykamera gleichmäßiges Licht, keine Perspektive und hohe Auflösung: die Erkennung ist damit deutlich zuverlässiger als per Kamera.

## Optionen für den Scanner-Zugriff

| Weg | Wie | Plattform | Aufwand | Zuverlässigkeit |
|---|---|---|---|---|
| **eSCL / AirScan** | HTTP-Protokoll direkt zum Scanner im WLAN/LAN (mDNS-Discovery `_uscan._tcp`, dann `ScanJobs` per XML) | alle, treiberlos | mittel (Rust- oder TS-Implementierung, ~500 Zeilen) | hoch bei Geräten ab ~2018 (HP, Canon, Epson, Brother) |
| **NAPS2 CLI** | Open-Source-Scan-Tool per Kommandozeile aufrufen, Ergebnisbild einlesen | Windows, macOS, Linux; WIA, TWAIN, SANE, eSCL | niedrig | hoch, aber externe Installation nötig |
| **Ordner-Import** | Nutzer scannt mit Herstellersoftware in einen Ordner; App überwacht ihn | alle | sehr niedrig | hoch, aber ein Klick mehr pro Seite |
| ImageCaptureCore | Apple-Framework | nur macOS, nur native App | niedrig (Swift) | hoch |
| WIA/TWAIN direkt | Windows-APIs über Rust/Node-Bindings | nur Windows | hoch | mittel (Treiberzoo) |

## Entscheidung (Vorschlag)

Stufenmodell in `apps/desktop`:
1. **Ordner-Import + Drag-and-drop** zuerst (Phase 2, Woche 1). Funktioniert mit jedem Scanner sofort und ist auch für Fotos vom Handy nützlich.
2. **eSCL direkt** als Standardweg (Phase 2). Kein Treiber, kein Zusatzprogramm, funktioniert unter Windows und macOS gleich.
3. **NAPS2-Fallback** für USB-only-Scanner ohne Netzwerk (Phase 3, optional).

## Verarbeitungspipeline

```
Scan (300 dpi, Farbe) → Hintergrund-Erkennung (Scannerdeckel = weiß/schwarz) → Konturen → Rechtecke mit 63:88-Verhältnis (±5 %)
→ Rotation korrigieren (0/90/180/270 anhand Textausrichtung/Hash-Vergleich) → pro Karte: Hash + OCR-Nummer → Match
→ Kontaktbogen-Ansicht: 9 Karten mit Treffer, Konfidenz, Variante/Zustand pro Karte setzbar → "Alle übernehmen"
```

- Empfehlung an Nutzer im UI: Karten mit Abstand ≥ 5 mm auflegen, dunkle Unterlage bei weißen Kartenrändern.
- Hüllen (Sleeves) erzeugen Reflexe; Toploader sind ok. Hinweis im UI.
- Zusätzlich möglich, weil Auflösung hoch: automatische **Zentrierungs-Messung** für den Pregrading-Check (E4) direkt aus dem Scan.

## Konsequenzen

- `packages/card-matcher` bekommt ein Modul `flatbed-segmentation` (reines TS auf Pixel-Arrays, testbar mit Beispielscans in `fixtures/`).
- Desktop-App braucht eine Scanner-Bridge in Tauri (Rust) für eSCL-Discovery und -Scan; alles andere bleibt TypeScript.
- Testgeräte: mindestens ein eSCL-fähiger Drucker-Scanner pro Entwickler; Modell und Ergebnis in `docs/` festhalten.
