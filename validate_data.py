import json
import re

def validate():
    try:
        with open('data.js', 'r', encoding='utf-8') as f:
            content = f.read()
            
        patterns = {
            "PLAYER_STATS": r'window\.PLAYER_STATS = (\[.*?\]);',
            "TEAM_CALENDARS": r'window\.TEAM_CALENDARS = (\{.*?\});',
            "MATCH_DETAILS": r'window\.MATCH_DETAILS = (\{.*\});'
        }
        
        for name, pattern in patterns.items():
            match = re.search(pattern, content, re.DOTALL)
            if match:
                try:
                    json.loads(match.group(1))
                    print(f"{name}: OK")
                except json.JSONDecodeError as e:
                    print(f"{name}: FAILED - {e}")
                    # Print context around error
                    start = max(0, e.pos - 50)
                    end = min(len(match.group(1)), e.pos + 50)
                    print(f"Context: ...{match.group(1)[start:end]}...")
            else:
                print(f"{name}: NOT FOUND")
                
    except Exception as e:
        print(f"Global Error: {e}")

if __name__ == "__main__":
    validate()
