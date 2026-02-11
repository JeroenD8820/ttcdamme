import requests
from bs4 import BeautifulSoup
import json
import os
import time

def scrape_match_detail(url):
    print(f"Scraping match detail: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Match info (Title, Date, Score)
        # Usually metadata is in og:description or titles
        title = soup.find('title').get_text(strip=True)
        
        # Players tables
        home_players = []
        home_players_div = soup.find('div', id='home_players')
        if home_players_div:
            table = home_players_div.find('table', class_='DBTable')
            if table:
                for row in table.find_all('tr')[1:]: # Skip header
                    cells = row.find_all('td')
                    if len(cells) >= 6:
                        home_players.append({
                            "id": cells[2].get_text(strip=True),
                            "name": cells[3].get_text(strip=True),
                            "classification": cells[4].get_text(strip=True),
                            "won": cells[5].get_text(strip=True)
                        })
                        
        away_players = []
        away_players_div = soup.find('div', id='away_players')
        if away_players_div:
            table = away_players_div.find('table', class_='DBTable')
            if table:
                for row in table.find_all('tr')[1:]: # Skip header
                    cells = row.find_all('td')
                    if len(cells) >= 6:
                        away_players.append({
                            "id": cells[2].get_text(strip=True),
                            "name": cells[3].get_text(strip=True),
                            "classification": cells[4].get_text(strip=True),
                            "won": cells[5].get_text(strip=True)
                        })
                        
        # Games results
        games = []
        results_list_table = soup.find('table', id='result_list')
        if results_list_table:
            for row in results_list_table.find_all('tr', class_='DBTable'):
                cells = row.find_all('td')
                if len(cells) >= 10:
                    sets = []
                    # S1 to S5 are cells 3 to 7
                    for i in range(3, 8):
                        val = cells[i].get_text(strip=True)
                        if val:
                            sets.append(val)
                            
                    games.append({
                        "home_player": cells[1].get_text(strip=True),
                        "away_player": cells[2].get_text(strip=True),
                        "sets": ", ".join(sets),
                        "result_sets": cells[8].get_text(strip=True),
                        "result_game": cells[9].get_text(strip=True)
                    })
                    
        return {
            "title": title,
            "home_players": home_players,
            "away_players": away_players,
            "games": games
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def main():
    if not os.path.exists('team_calendars.json'):
        print("team_calendars.json not found.")
        return
        
    with open('team_calendars.json', 'r', encoding='utf-8') as f:
        calendars = json.load(f)
        
    # To avoid repeated scraping of the same match (though unlikely here)
    # or just to keep track
    all_details = {}
    
    # We only scrape played matches (those with a score like "09 - 07")
    # And we'll limit it to avoid too many requests at once during dev
    
    # Actually, let's scrape them all but maybe add a small delay
    total_matches = 0
    for team, matches in calendars.items():
        for match in matches:
            if match.get('url') and match.get('score') and '-' in match['score']:
                match_id = match['match_id']
                if match_id not in all_details:
                    # Let's check if we already have it (basic caching)
                    # For now just scrape
                    details = scrape_match_detail(match['url'])
                    if details:
                        all_details[match_id] = details
                    total_matches += 1
                    time.sleep(0.5) # Be nice to the server
                    
    # Save to JSON
    with open('match_details.json', 'w', encoding='utf-8') as f:
        json.dump(all_details, f, indent=4, ensure_ascii=False)
    print(f"Saved {len(all_details)} match reports to match_details.json")

    # Update data.js for local dashboard usage (CORS fix)
    try:
        import json_to_js
        json_to_js.convert()
    except Exception as e:
        print(f"Warning: Could not update data.js: {e}")

if __name__ == "__main__":
    main()
