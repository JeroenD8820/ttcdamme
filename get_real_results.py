import requests
from bs4 import BeautifulSoup
import json
import re

def get_matches(div_id, week=15):
    url = f"https://competitie.vttl.be/index.php?club_id=65&div_id={div_id}&menu=5&withres=1&week_name={week}"
    print(f"Fetching {url}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for the match table
        tables = soup.find_all('table', class_='DBTable')
        matches = []
        for table in tables:
            headers = [th.get_text(strip=True) for th in table.find_all('th')]
            if "Wedstrijd" in headers and "Thuis" in headers:
                rows = table.find_all('tr')[1:] # Skip header
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        match_id = cols[0].get_text(strip=True)
                        home = cols[1].get_text(strip=True)
                        away = cols[2].get_text(strip=True)
                        score = cols[3].get_text(strip=True)
                        
                        # Check if it involves Damme
                        if "Damme" in home or "Damme" in away:
                            # Try to find a date if possible? (Usually not on this page)
                            # We'll assume the date of Week 15 (Feb 7/8 2026)
                            matches.append({
                                "id": match_id,
                                "home": home,
                                "away": away,
                                "score": score
                            })
                break
        return matches
    except Exception as e:
        print(f"Error fetching {div_id}: {e}")
        return []

def main():
    divisions = {
        "A": "8731",
        "B": "8736",
        "C": "8738",
        "D": "8737"
    }
    
    all_matches = []
    for team, div_id in divisions.items():
        print(f"Processing Ploeg {team}...")
        results = get_matches(div_id)
        for r in results:
            # Clean up score and determine result
            score = r["score"].replace("\u00a0", " ")
            res_type = "draw"
            if " - " in score:
                try:
                    p1, p2 = map(int, score.split(" - "))
                    if "Damme" in r["home"]:
                        res_type = "win" if p1 > p2 else ("loss" if p2 > p1 else "draw")
                    else:
                        res_type = "win" if p2 > p1 else ("loss" if p1 > p2 else "draw")
                except:
                    pass
            
            all_matches.append({
                "date": "07/02/2026", # Default for week 15
                "home": r["home"],
                "away": r["away"],
                "score": score,
                "result": res_type
            })
            
    print(f"Found {len(all_matches)} matches.")
    # Sort them? Maybe later.
    
    with open("real_results.json", "w", encoding="utf-8") as f:
        json.dump(all_matches, f, indent=4)
    print("Results saved to real_results.json")

if __name__ == "__main__":
    main()
