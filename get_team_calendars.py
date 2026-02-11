import requests
from bs4 import BeautifulSoup
import json
import re

def get_match_data_from_per_team(div_id):
    """
    Scrapes the 'Per Ploeg' view to get Match IDs, Teams, and Scores.
    """
    url = f"https://competitie.vttl.be/?menu=4&club_id=65&perteam=1&div_id={div_id}"
    print(f"Scraping 'Per Ploeg' scores for {div_id}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        matches = {}
        # Find the "Resultaten" subtitle and then the table
        subtitle_td = soup.find("td", string="Resultaten")
        if not subtitle_td:
            # Fallback: maybe it's in a different tag or has spaces
            subtitle_td = soup.find(lambda tag: tag.name == "td" and "Resultaten" in tag.text)
            
        if not subtitle_td:
            print(f"Warning: 'Resultaten' subtitle not found for {div_id}")
            return {}
            
        # The table is a sibling of the wrapper div
        wrapper_div = subtitle_td.find_parent("div", class_="interclubs_subtitle_wrapper")
        if not wrapper_div:
            print(f"Warning: wrapper div not found for {div_id}")
            return {}
            
        results_table = wrapper_div.find_next_sibling("table", class_="DBTable_short")
        if not results_table:
            print(f"Warning: results table not found for {div_id}")
            return {}
            
        for row in results_table.find_all("tr", class_="DBTable_short"):
            cells = row.find_all("td")
            if len(cells) < 4:
                continue
                
            match_id_cell = cells[0]
            link = match_id_cell.find("a")
            # If there's no link, it might not be a match row (header or sum)
            if not link:
                continue
                
            match_id = match_id_cell.get_text(strip=True)
            match_url = link['href'] if link else None
            
            home_team = cells[1].get_text(strip=True)
            away_team = cells[2].get_text(strip=True)
            score = cells[3].get_text(strip=True).replace('\xa0', ' ')
            
            matches[match_id] = {
                "match_id": match_id,
                "url": match_url,
                "home_team": home_team,
                "away_team": away_team,
                "score": score
            }
        return matches
    except Exception as e:
        print(f"Error scraping scores for {div_id}: {e}")
        return {}

def get_dates_from_season_view(div_id):
    """
    Scrapes the 'Season' view (menu 3) to get Match IDs, Dates, and Times.
    """
    clean_div_id = div_id.split('_')[0]
    url = f"https://competitie.vttl.be/?menu=3&type=3&div_id={clean_div_id}&club_id=65"
    print(f"Scraping 'Season' dates for {div_id}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        dates = {}
        # Dates are in many short tables grouped by week
        for row in soup.find_all("tr", class_="DBTable_short"):
            cells = row.find_all("td")
            if len(cells) < 4:
                continue
            
            match_id = cells[0].get_text(strip=True)
            if match_id in ["Wedstrijd", "Datum", "Thuis", "Bezoekers"]:
                continue
                
            date_time = cells[1].get_text(strip=True).replace('\xa0', ' ')
            home_team = cells[2].get_text(strip=True)
            away_team = cells[3].get_text(strip=True)
            
            date = "Unknown"
            time = "Unknown"
            if " / " in date_time:
                parts = date_time.split(" / ")
                date = parts[0].strip()
                time = parts[1].strip()
            elif date_time:
                date = date_time.strip()
                
            dates[match_id] = {
                "date": date,
                "time": time,
                "home_team": home_team,
                "away_team": away_team
            }
        return dates
    except Exception as e:
        print(f"Error scraping dates for {div_id}: {e}")
        return {}

def main():
    teams = {
        "A": "8731_A",
        "B": "8736_B",
        "C": "8738_C",
        "D": "8737_D"
    }
    
    all_calendars = {}
    for team_letter, div_id in teams.items():
        scores_data = get_match_data_from_per_team(div_id)
        dates_data = get_dates_from_season_view(div_id)
        
        combined_matches = []
        # We iterate over dates_data because it contains all matches for the division
        for match_id, date_info in dates_data.items():
            # Capture ALL matches in the division (not just Damme)
            combined = {
                "match_id": match_id,
                "home_team": date_info["home_team"],
                "away_team": date_info["away_team"],
                "date": date_info["date"],
                "time": date_info["time"],
                "score": "",
                "url": None
            }
            
            # If we have score data for this match, add it
            if match_id in scores_data:
                combined["score"] = scores_data[match_id]["score"]
                combined["url"] = scores_data[match_id]["url"]
            
            combined_matches.append(combined)
            
        all_calendars[team_letter] = combined_matches
        
    # Save to JSON
    with open('team_calendars.json', 'w', encoding='utf-8') as f:
        json.dump(all_calendars, f, indent=4)
    print(f"Saved {sum(len(m) for m in all_calendars.values())} matches to team_calendars.json")

    # Update data.js for local dashboard usage (CORS fix)
    try:
        import json_to_js
        json_to_js.convert()
    except Exception as e:
        print(f"Warning: Could not update data.js: {e}")

if __name__ == "__main__":
    main()
