import requests
from bs4 import BeautifulSoup
import json
import re
import time

def normalize_name(name):
    parts = name.strip().upper().split()
    if not parts: return ""
    parts.sort()
    return " ".join(parts)

def get_player_data(frenoy_id):
    url = f"https://competitie.vttl.be/speler/{frenoy_id}/uitslagen/1"
    print(f"Fetching data for {frenoy_id}...")
    data = {"elo": 0, "relative": 0}
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Get Elo
        elo_td = soup.find('td', class_=lambda x: x and 'elo' in x.split())
        if elo_td:
            val_span = elo_td.find('span', class_='value')
            if val_span:
                try:
                    data["elo"] = int(val_span.text.strip().replace('.', ''))
                except: pass
        
        # 2. Get Relative points
        # Find the row containing "Relatieve punten"
        for tr in soup.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) >= 2:
                if "Relatieve punten" in tds[0].text:
                    try:
                        data["relative"] = int(tds[1].text.strip())
                    except: pass
        
        # 3. Get Classification
        # Find the row containing "Rangschikking"
        for tr in soup.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) >= 1:
                if "Rangschikking" in tds[0].text and ":" in tds[0].text:
                    data["classification"] = tds[0].text.split(":")[-1].strip()

    except Exception as e:
        print(f"Error fetching {frenoy_id}: {e}")
    return data

def main():
    existing_players = [
        {"memberId": "512926", "name": "JASPER MAHIEU", "frenoyId": "37491"},
        {"memberId": "512925", "name": "GERT-JAN MAHIEU", "frenoyId": "37490"},
        {"memberId": "500783", "name": "MICHIEL KEMPINCK", "frenoyId": "11497"},
        {"memberId": "501549", "name": "DAAN DE JAEGHERE", "frenoyId": "11681"},
        {"memberId": "514169", "name": "BART VANDERPLAETSE", "frenoyId": "41895"},
        {"memberId": "513374", "name": "VICTOR VANHOVE", "frenoyId": "39178"},
        {"memberId": "500981", "name": "KRISTOF ADAM", "frenoyId": "11561"},
        {"memberId": "504715", "name": "GWEN GRIJP", "frenoyId": "8879"},
        {"memberId": "535114", "name": "BRIEK REYBROUCK", "frenoyId": "119697"},
        {"memberId": "535166", "name": "IAN ROBBERECHTS", "frenoyId": "119969"},
        {"memberId": "534291", "name": "MARIA-HELENA FACK", "frenoyId": "115103"},
        {"memberId": "536044", "name": "OLIVER VANAGT", "frenoyId": "125347"},
        {"memberId": "535947", "name": "HANNE VAN BUYLAERE", "frenoyId": "125339"},
        {"memberId": "535948", "name": "ROBBE VAN BUYLAERE", "frenoyId": "125341"},
        {"memberId": "535946", "name": "ANDREAS JACXSENS", "frenoyId": "124291"},
        {"memberId": "530516", "name": "DAVE IDE", "frenoyId": "96101"},
        {"memberId": "534289", "name": "NAND HERNOU", "frenoyId": "115155"},
        {"memberId": "501132", "name": "REGINE PHARASYN", "frenoyId": "11603"},
        {"memberId": "527709", "name": "JOHAN MALFRERE", "frenoyId": "84655"},
        {"memberId": "513960", "name": "LUC MAHIEU", "frenoyId": "41516"},
        {"memberId": "530496", "name": "MILAN MORTIER", "frenoyId": "96111"},
        {"memberId": "517743", "name": "WOUTER JANSSENS", "frenoyId": "54442"},
        {"memberId": "501134", "name": "JEAN-PIERRE DEFOUR", "frenoyId": "11604"},
        {"memberId": "526292", "name": "BART D'HOORE", "frenoyId": "77261"},
        {"memberId": "532356", "name": "JENTE PAREYN", "frenoyId": "105565"},
        {"memberId": "532355", "name": "JELLE PAREYN", "frenoyId": "105563"},
        {"memberId": "524879", "name": "SARI BLONDEEL", "frenoyId": "73688"},
        {"memberId": "531918", "name": "LUCAS DOMBRECHT", "frenoyId": "103069"},
        {"memberId": "527606", "name": "JEROEN DOMBRECHT", "frenoyId": "81329"},
        {"memberId": "526291", "name": "KURT D'HOORE", "frenoyId": "77260"},
        {"memberId": "513031", "name": "JEROEN CATTOOR", "frenoyId": "37807"},
        {"memberId": "500969", "name": "PASCAL HUYBRECHS", "frenoyId": "11557"},
        {"memberId": "534290", "name": "JORIS HERNOU", "frenoyId": "77259"}
    ]
    
    results = []
    for p in existing_players:
        player_data = get_player_data(p['frenoyId'])
        
        results.append({
            "name": p['name'],
            "memberId": p['memberId'],
            "frenoyId": p['frenoyId'],
            "elo": player_data.get("elo", 0),
            "relative": player_data.get("relative", 0),
            "classification": player_data.get("classification", "NG")
        })
        time.sleep(1)
        
    with open("final_player_stats.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    print(f"Saved {len(results)} players to final_player_stats.json")

if __name__ == "__main__":
    main()
