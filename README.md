# TTC Damme Dashboard (WVL158)

Moderne webapplicatie voor rangschikkingen en resultaten van TTC Damme.

## Hoe de app starten

**Optie A – Eenvoudig (bestand in browser openen):**
Dubbelklik op `index.html`. Werkt zonder server, maar de "Ververs" knop herlaadt alleen de pagina.

**Optie B – Met lokale server (aanbevolen):**
Dubbelklik op `start_server.bat`, open dan `http://localhost:5000` in je browser.
De "Ververs" knop haalt nu écht nieuwe data op van VTTL.

---

## Data updaten

### Methode 1: Handmatig (eenmalig)
Dubbelklik op **`update_data.bat`**.
Dit script haalt alle data op van VTTL en vernieuwt `data.js`.
Duur: ±2–5 minuten.

### Methode 2: Via de "Ververs" knop (lokale server)
1. Start de server via **`start_server.bat`**
2. Open `http://localhost:5000` in de browser
3. Klik op de 🔄 knop rechtsboven
4. Wacht op de groene melding "Data bijgewerkt"

### Methode 3: Automatisch via GitHub Actions
Als de app in een GitHub repository staat, draait de workflow in `.github/workflows/update_data.yml` automatisch elke dag om 07:00 en 23:00 (Belgische tijd).

**Setup vereisten:**
1. Maak een GitHub repository aan en push de code
2. Ga naar **Settings → Pages** en stel de bron in op de `main` branch
3. De workflow draait dan automatisch en commit nieuwe `data.js` na elke update

Je kan de workflow ook handmatig starten via: **GitHub → Actions → Update TTC Damme Data → Run workflow**

---

## Projectstructuur

| Bestand | Beschrijving |
|---|---|
| `index.html` | Hoofd dashboard pagina |
| `app.js` | Dashboard logica |
| `style.css` | Styling |
| `data.js` | Gegenereerde data (niet handmatig bewerken) |
| `update_data.bat` | Handmatig data updaten |
| `start_server.bat` | Lokale Flask server starten |
| `server.py` | Flask server met `/api/update` endpoint |
| `get_all_rankings.py` | Spelersstats ophalen van VTTL |
| `get_team_calendars.py` | Teamkalenders ophalen |
| `get_match_details.py` | Wedstrijddetails ophalen |
| `json_to_js.py` | JSON → data.js converter |
| `.github/workflows/` | GitHub Actions automatisering |
