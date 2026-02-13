import requests
from bs4 import BeautifulSoup
import json
import random
from datetime import datetime

SEARCH_QUERY = "Software Entwickler"
LOCATION = "Schweiz"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

def scrape():
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    url = "https://www.careerjet.ch/search/results.html"
    params = {"s": SEARCH_QUERY, "l": LOCATION, "sort": "date"}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=20)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs = []
            for item in soup.select('article.job, .job'):
                title_el = item.select_one('h2 a, .title a')
                if title_el:
                    link = title_el['href']
                    if link.startswith('/'): link = "https://www.careerjet.ch" + link
                    jobs.append({
                        "title": title_el.get_text(strip=True),
                        "link": link,
                        "company": item.select_one('.company_name, .company').get_text(strip=True) if item.select_one('.company_name, .company') else "Unbekannt",
                        "location": item.select_one('.location').get_text(strip=True) if item.select_one('.location') else "Schweiz",
                        "scraped_at": datetime.now().strftime("%d.%m.%Y %H:%M")
                    })
            
            with open('jobs.json', 'w', encoding='utf-8') as f:
                json.dump(jobs, f, ensure_ascii=False, indent=4)
            print(f"Erfolg: {len(jobs)} Jobs gespeichert.")
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    scrape()
