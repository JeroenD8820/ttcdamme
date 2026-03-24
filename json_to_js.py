import json
import os

def convert():
    # Gebruik de map waar dit script in staat, in plaats van een hardcoded pad
    data_dir = os.path.dirname(os.path.abspath(__file__))
    
    files = {
        "PLAYER_STATS": "scraped_player_stats.json",
        "TEAM_CALENDARS": "team_calendars.json",
        "MATCH_DETAILS": "match_details.json"
    }
    
    js_content = "/** TTC Damme Data Storage **/\n\n"
    
    for var_name, filename in files.items():
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                js_content += f"window.{var_name} = {json.dumps(data, indent=2)};\n\n"
        else:
            print(f"Warning: {filename} not found.")
            js_content += f"window.{var_name} = {{}};\n\n"
            
    output_path = os.path.join(data_dir, "data.js")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"Successfully created {output_path}")

if __name__ == "__main__":
    convert()
