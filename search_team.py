import requests
from bs4 import BeautifulSoup
import time

def find_damme_teams():
    for i in range(8720, 8800):
        url = f"https://competitie.vttl.be/?menu=3&div_id={i}"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                title = soup.find('title').text
                # Find any text containing "Damme" in DBTable cells
                damme_mentions = [td.text.strip() for td in soup.find_all('td', class_='DBTable') if 'Damme' in td.text]
                if damme_mentions:
                    print(f"ID {i}: {title} -> {damme_mentions}")
            time.sleep(0.1) # Be nice
        except Exception as e:
            print(f"Error for {i}: {e}")

if __name__ == "__main__":
    find_damme_teams()
