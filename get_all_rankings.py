import requests
from bs4 import BeautifulSoup
import json
import re

def normalize_name(name):
    # Remove extra whitespace and convert to upper
    parts = name.strip().upper().split()
    if not parts:
        return ""
    # We want to handle both "FIRST LAST" and "LAST FIRST"
    # Actually, VTTL usually has "LAST FIRST" in some views and "FIRST LAST" in others.
    # We'll just sort the words alphabetically to create a canonical key
    parts.sort()
    return " ".join(parts)

def scrape_rankings(url):
    print(f"Scraping {url}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='DBTable')
    if not table:
        print("Table 'DBTable' not found.")
        return []

    rows = table.find_all('tr', class_='DBTable')
    players = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 4:
            name_cell = cols[1]
            raw_name = name_cell.get_text(strip=True)
            link = name_cell.find('a')
            member_frenoy_id = ""
            if link:
                href = link.get('href', '')
                match = re.search(r'/speler/(\d+)/', href)
                if match:
                    member_frenoy_id = match.group(1)
            
            classification = cols[2].get_text(strip=True)
            points = cols[3].get_text(strip=True)
            
            players.append({
                "rawName": raw_name,
                "name": normalize_name(raw_name),
                "classification": classification,
                "points": int(points) if points.replace('-', '').isdigit() else 0,
                "frenoyId": member_frenoy_id
            })
    return players

def main():
    merged = {}
    
    # Scrape Relative Rankings
    page = 1
    while True:
        players = scrape_rankings(f"https://competitie.vttl.be/?menu=5&relative=1&club=WVL158&club_id=65&cur_page={page}")
        if not players:
            break
        for p in players:
            key = p['name']
            merged[key] = {
                "name": p['rawName'],
                "classification": p['classification'],
                "relative": p['points'],
                "elo": 0,
                "frenoyId": p['frenoyId']
            }
        page += 1
        if page > 5: break # Safety
        
    # Scrape Elo Rankings
    page = 1
    while True:
        players = scrape_rankings(f"https://competitie.vttl.be/?menu=5&elo=1&club=WVL158&club_id=65&cur_page={page}")
        if not players:
            break
        for p in players:
            key = p['name']
            if key in merged:
                merged[key]['elo'] = p['points']
                if not merged[key]['frenoyId']:
                    merged[key]['frenoyId'] = p['frenoyId']
            else:
                merged[key] = {
                    "name": p['rawName'],
                    "classification": p['classification'],
                    "relative": 0,
                    "elo": p['points'],
                    "frenoyId": p['frenoyId']
                }
        page += 1
        if page > 5: break # Safety

    output = sorted(list(merged.values()), key=lambda x: x['name'])

    with open("scraped_player_stats.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)
    print(f"Saved {len(output)} players to scraped_player_stats.json")

if __name__ == "__main__":
    main()
