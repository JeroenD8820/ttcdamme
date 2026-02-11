import os
import json
import re
from bs4 import BeautifulSoup

def normalize_name(name):
    if not name:
        return ""
    # Convert to uppercase, split into words, sort them, and rejoin
    # This handles "First Last" vs "Last First"
    words = name.strip().upper().split()
    words.sort()
    return " ".join(words)

def parse_players(files):
    players = {}
    for file in files:
        if not os.path.exists(file):
            print(f"Warning: {file} not found")
            continue
        
        print(f"Parsing {file}...")
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f, 'html.parser')
            # Look for the table that contains actual player data
            tables = soup.find_all('table', class_='DBTable')
            target_table = None
            for t in tables:
                if t.get('id') == 'pfilters':
                    continue
                # The headers should contain "Lidnummer" or "Index"
                if "Index" in t.get_text() or "Lidnummer" in t.get_text():
                    target_table = t
                    break
            
            if not target_table:
                print(f"No player table found in {file}")
                continue
            
            rows = target_table.find_all('tr')
            print(f"Found {len(rows)} rows in {file}")
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 6:
                    member_id = cols[1].get_text(strip=True)
                    # Use the full name column (index 4 in the VTTL player list)
                    name = cols[4].get_text(strip=True)
                    classification = cols[5].get_text(strip=True)
                    
                    if not member_id.isdigit():
                        continue
                        
                    norm_name = normalize_name(name)
                    if norm_name:
                        # Store both the cleaned name and the original name for display
                        players[norm_name] = {
                            "memberId": member_id,
                            "name": name,
                            "classification": classification,
                            "elo": 0,
                            "relative": 0
                        }
    print(f"Master list has {len(players)} players")
    return players

def parse_elo(file, players):
    if not os.path.exists(file):
        print(f"Warning: {file} not found")
        return
    
    with open(file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        table = soup.find('table', class_='DBTable')
        if not table:
            return
        
        rows = table.find_all('tr', class_='DBTable')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                name = cols[1].get_text(strip=True)
                elo = cols[3].get_text(strip=True)
                
                norm_name = normalize_name(name)
                if norm_name in players:
                    try:
                        players[norm_name]["elo"] = int(elo)
                    except ValueError:
                        pass
                else:
                    # Some players might only be in rankings? (shouldn't happen for club filter)
                    print(f"Elo player not found in master list: {name}")

def parse_relative(file, players):
    if not os.path.exists(file):
        print(f"Warning: {file} not found")
        return
    
    with open(file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        table = soup.find('table', class_='DBTable')
        if not table:
            return
        
        rows = table.find_all('tr', class_='DBTable')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                name = cols[1].get_text(strip=True)
                relative = cols[3].get_text(strip=True)
                
                norm_name = normalize_name(name)
                if norm_name in players:
                    try:
                        players[norm_name]["relative"] = int(relative)
                    except ValueError:
                        pass
                else:
                    print(f"Relative player not found in master list: {name}")

def main():
    player_files = ['players_fixed.html', 'players_page2.html']
    elo_file = 'elo_rankings.html'
    relative_file = 'relative_rankings.html'
    
    players = parse_players(player_files)
    parse_elo(elo_file, players)
    parse_relative(relative_file, players)
    
    # Convert back to list and sort by elo
    player_list = list(players.values())
    player_list.sort(key=lambda x: x['elo'], reverse=True)
    
    with open('players.json', 'w', encoding='utf-8') as f:
        json.dump(player_list, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully processed {len(player_list)} players to players.json")

if __name__ == "__main__":
    main()
