import requests
from bs4 import BeautifulSoup
import json

def get_full_ranking(div_id):
    url = f"https://competitie.vttl.be/index.php?club_id=65&div_id={div_id}&menu=5"
    print(f"Fetching ranking for {div_id}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for the ranking table (it's the second DBTable usually, but let's be safe)
        tables = soup.find_all('table', class_='DBTable')
        ranking = []
        for table in tables:
            headers = [th.get_text(strip=True) for th in table.find_all('th')]
            if "AW" in headers and "Ploegnaam" in headers:
                rows = table.find_all('tr')[1:] # Skip header
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 10:
                        ranking.append({
                            "position": cols[0].get_text(strip=True),
                            "team": cols[1].get_text(strip=True),
                            "matches": cols[2].get_text(strip=True),
                            "wins": cols[3].get_text(strip=True),
                            "losses": cols[4].get_text(strip=True),
                            "draws": cols[5].get_text(strip=True),
                            "points": cols[11].get_text(strip=True) if len(cols) > 11 else cols[-1].get_text(strip=True)
                        })
                break
        return ranking
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    divisions = {
        "Damme A": "8731",
        "Damme B": "8736",
        "Damme C": "8738",
        "Damme D": "8737"
    }
    
    data = {}
    for team, div_id in divisions.items():
        data[team] = get_full_ranking(div_id)
        
    with open("full_rankings.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print("Full rankings saved to full_rankings.json")

if __name__ == "__main__":
    main()
