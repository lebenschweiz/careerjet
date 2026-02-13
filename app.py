from flask import Flask, render_template_string
import json
import os

app = Flask(__name__)

def load_jobs():
    """Lädt die Job-Daten aus der durch GitHub Actions erzeugten JSON-Datei."""
    file_path = "jobs.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if data else []
        except Exception as e:
            print(f"Fehler beim Lesen der JSON-Datei: {e}")
            return []
    return []

@app.route('/')
def index():
    """Hauptseite der App, die die gespeicherten Jobs anzeigt."""
    jobs = load_jobs()
    
    # Bestimmung der letzten Aktualisierung (vom ersten Job in der Liste)
    last_update = jobs[0].get('scraped_at', 'Unbekannt') if jobs else "Noch kein Update erfolgt"

    html_template = """
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Job-Radar Schweiz</title>
        <style>
            :root {
                --primary: #cc0000;
                --secondary: #2563eb;
                --bg: #f1f5f9;
                --card-bg: #ffffff;
                --text-main: #0f172a;
                --text-muted: #64748b;
            }
            body { 
                font-family: 'Inter', -apple-system, sans-serif; 
                background-color: var(--bg); 
                color: var(--text-main); 
                margin: 0; 
                padding: 20px; 
                line-height: 1.6;
            }
            .container { max-width: 900px; margin: 0 auto; }
            header { 
                background: var(--primary); 
                color: white; 
                padding: 40px 20px; 
                border-radius: 16px; 
                text-align: center; 
                margin-bottom: 30px; 
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            }
            h1 { margin: 0; font-size: 2.5rem; }
            .update-badge {
                display: inline-block;
                background: rgba(255, 255, 255, 0.2);
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.85rem;
                margin-top: 10px;
            }
            .job-grid { display: grid; gap: 20px; }
            .job-card { 
                background: var(--card-bg); 
                padding: 25px; 
                border-radius: 12px; 
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
                border-left: 6px solid var(--primary);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .job-card:hover { 
                transform: translateY(-4px); 
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            }
            .title { 
                font-size: 1.4rem; 
                font-weight: 700; 
                color: var(--secondary); 
                text-decoration: none; 
                display: block; 
                margin-bottom: 8px;
            }
            .meta { 
                display: flex;
                gap: 20px;
                font-size: 0.95rem; 
                color: var(--text-muted); 
                margin-bottom: 15px;
                font-weight: 500;
            }
            .description { 
                font-size: 1rem; 
                color: #334155;
                display: -webkit-box;
                -webkit-line-clamp: 3;
                -webkit-box-orient: vertical;
                overflow: hidden;
            }
            .btn { 
                display: inline-block; 
                margin-top: 20px; 
                padding: 10px 20px; 
                background: var(--primary); 
                color: white; 
                text-decoration: none; 
                border-radius: 8px; 
                font-weight: 600; 
                font-size: 0.95rem;
                transition: opacity 0.2s;
            }
            .btn:hover { opacity: 0.9; }
            .no-jobs { 
                text-align: center; 
                padding: 60px 20px; 
                background: white; 
                border-radius: 16px; 
                color: var(--text-muted);
            }
            footer {
                text-align: center;
                margin-top: 50px;
                color: var(--text-muted);
                font-size: 0.85rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🇨🇭 Job-Radar Schweiz</h1>
                <div class="update-badge">Letzte Aktualisierung: {{ last_update }}</div>
            </header>

            <div class="job-grid">
            {% if jobs %}
                {% for job in jobs %}
                <div class="job-card">
                    <a href="{{ job.link }}" target="_blank" class="title">{{ job.title }}</a>
                    <div class="meta">
                        <span>🏢 {{ job.company }}</span>
                        <span>📍 {{ job.location }}</span>
                    </div>
                    <div class="description">{{ job.description }}</div>
                    <a href="{{ job.link }}" target="_blank" class="btn">Vollständiges Inserat</a>
                </div>
                {% endfor %}
            {% else %}
                <div class="no-jobs">
                    <h2>Noch keine Jobs geladen</h2>
                    <p>Die <strong>jobs.json</strong> wurde noch nicht generiert. Bitte starte die GitHub Action manuell oder warte auf den nächsten automatischen Durchlauf.</p>
                </div>
            {% endif %}
            </div>
            
            <footer>
                Erstellt für die Jobsuche in der Schweiz. Daten bereitgestellt via GitHub Actions & Careerjet Scraper.
            </footer>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, jobs=jobs, last_update=last_update)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
