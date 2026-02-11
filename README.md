# TTC Damme Dashboard (WVL158)

Dit is een moderne webapplicatie om de rangschikking en resultaten van TTC Damme weer te geven.

## Hoe te starten
1. Ga naar de map `C:\Users\JeroenDombrecht\.gemini\antigravity\scratch\ttc-damme-app`.
2. Klik met de rechtermuisknop op `index.html` en kies **Openen met** > **Google Chrome** (of een andere moderne browser).

## Kenmerken
- **Modern Design**: Glassmorphism effecten en dark mode.
- **Responsief**: Werkt op desktop en mobiel.
- **Data**: Toont momenteel de rangschikking van ploegen A t/m E en recente resultaten.

## Opmerking over Live Data
De applicatie bevat nu alle spelersgegevens direct in de code (`app.js`). Hierdoor werkt de app direct wanneer u `index.html` opent, zonder dat er een lokale server of internetverbinding nodig is voor de ledenlijst.

Voor een toekomstige volledige live-koppeling (real-time updates van VTTL) kan de `fetch` methode weer geactiveerd worden.
