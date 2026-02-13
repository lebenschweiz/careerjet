import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string
import os

app = Flask(__name__)

# --- KONFIGURATION ---
# Hier kannst du deine Suche anpassen
SEARCH_QUERY = "Software Entwickler"
LOCATION = "Zürich"

def get_jobs_via_scraping():
    # Careerjet Such-URL
    url = f"https://www.careerjet.ch/ws/suche/l/s.html?s={SEARCH_QUERY}&l={LOCATION}"
    
    # Wichtig: Ein echter User-Agent simuliert einen normalen Browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "de-CH,de;q=0.9,en;q=0.8"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        job_list = []
        
        # Careerjet Struktur (Stand heute)
        # Wir suchen nach allen Artikel-Elementen mit der Klasse 'job'
        articles = soup.select('article.job')

        for article in articles:
            # Titel und Link extrahieren
            title_link = article.select_one('header h2 a')
            if not title_link: continue
            
            title = title_link.get_text(strip=True)
            link = title_link['href']
            if link.startswith('/'):
                link = "https://www.careerjet.ch" + link
            
            # Firma extrahieren
            company = article.select_one('.company_name')
            company_text = company.get_text(strip=True) if company else "Nicht angegeben"
            
            # Ort extrahieren
            location = article.select_one('.location')
            location_text = location.get_text(strip=True) if location else "Schweiz"
            
            # Beschreibung extrahieren (Snippet)
            description = article.select_one('.desc')
            description_text = description.get_text(strip=True) if description else "Keine Kurzbeschreibung verfügbar."

            job_list.append({
                "title": title,
                "link": link,
                "company": company_text,
                "location": location_text,
                "description": description_text
            })
            
        return job_list
    except Exception as e:
        print(f"Scraping Fehler: {e}")
        return []

@app.route('/')
def index():
    jobs = get_jobs_via_scraping()
    
    html_template = """
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mein Job Radar</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; margin: 0; padding: 20px; color: #333; }
            .container { max-width: 900px; margin: 0 auto; }
            .header { text-align: center; padding: 40px 0; background: #cc0000; color: white; border-radius: 12px; margin-bottom: 30px; }
            .job-card { background: white; border-radius: 10px; padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: transform 0.2s; }
            .job-card:hover { transform: translateY(-3px); box-shadow: 0 6px 12px rgba(0,0,0,0.1); }
            .job-title { color: #cc0000; font-size: 1.4em; font-weight: bold; text-decoration: none; display: block; }
            .job-meta { margin: 10px 0; font-size: 0.9em; color: #666; font-weight: 600; }
            .job-desc { line-height: 1.6; color: #444; margin-bottom: 15px; }
            .btn { display: inline-block; background: #cc0000; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; }
            .footer { text-align: center; font-size: 0.8em; color: #999; margin-top: 50px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Job-Radar Schweiz</h1>
                <p>Aktuelle Stellen live von Careerjet</p>
            </div>
            
            {% if not jobs %}
            <div class="job-card">
                <p>Momentan konnten keine Jobs geladen werden. Bitte versuche es in wenigen Minuten erneut.</p>
            </div>
            {% endif %}

            {% for job in jobs %}
            <div class="job-card">
                <a href="{{ job.link }}" target="_blank" class="job-title">{{ job.title }}</a>
                <div class="job-meta">🏢 {{ job.company }} | 📍 {{ job.location }}</div>
                <div class="job-desc">{{ job.description }}</div>
                <a href="{{ job.link }}" target="_blank" class="btn">Details anzeigen</a>
            </div>
            {% endfor %}
            
            <div class="footer">Datenquelle: Careerjet.ch Scraper</div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, jobs=jobs)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
