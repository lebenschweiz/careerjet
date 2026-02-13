from flask import Flask, render_template_string
import json
import os

app = Flask(__name__)

# Pfad zur Datendatei, die von der GitHub Action erstellt wird
JOBS_FILE = "jobs.json"

def load_jobs_from_json():
    """Lädt die Jobdaten aus der lokalen JSON-Datei."""
    if os.path.exists(JOBS_FILE):
        try:
            with open(JOBS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Fehler beim Lesen der JSON: {e}")
            return []
    return []

@app.route('/')
def index():
    """Hauptseite der App, die Daten aus der JSON anzeigt."""
    jobs = load_jobs_from_json()
    
    # Zeitstempel der Datei auslesen für die Anzeige
    last_update = "Unbekannt"
    if os.path.exists(JOBS_FILE):
        import datetime
        mtime = os.path.getmtime(JOBS_FILE)
        last_update = datetime.datetime.fromtimestamp(mtime).strftime('%d.%m.%Y %H:%M:%S')

    html_template = """
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Job-Radar Schweiz (Offline-First)</title>
        <style>
            :root { 
                --primary: #cc0000; 
                --bg: #f1f5f9; 
                --text: #0f172a; 
            }
            body { 
                font-family: 'Inter', system-ui, sans-serif; 
                background: var(--bg); 
                color: var(--text); 
                margin: 0;
                padding: 20px; 
            }
            .container { max-width: 800px; margin: 0 auto; }
            header { 
                background: var(--primary); 
                color: white; 
                padding: 25px; 
                border-radius: 12px; 
                text-align: center; 
                margin-bottom: 25px;
            }
            .update-tag {
                font-size: 0.75rem;
                background: rgba(0,0,0,0.2);
                padding: 4px 10px;
                border-radius: 20px;
                display: inline-block;
                margin-top: 10px;
            }
            .job-card { 
                background: white; 
                padding: 20px; 
                margin-bottom: 15px; 
                border-radius: 10px; 
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                border-left: 5px solid var(--primary);
            }
            .title { 
                font-size: 1.2rem; 
                font-weight: bold; 
                color: #2563eb; 
                text-decoration: none; 
            }
            .meta { 
                font-size: 0.85rem; 
                color: #64748b; 
                margin: 8px 0;
            }
            .btn { 
                display: inline-block; 
                margin-top: 10px; 
                padding: 8px 16px; 
                background: var(--primary); 
                color: white; 
                text-decoration: none; 
                border-radius: 6px;
                font-size: 0.9rem;
            }
            .empty-state {
                text-align: center;
                background: white;
                padding: 50px;
                border-radius: 12px;
                border: 2px dashed #cbd5e1;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🇨🇭 Job-Radar Schweiz</h1>
                <div class="update-tag">Letztes Update: {{ last_update }}</div>
            </header>

            {% if jobs %}
                {% for job in jobs %}
                <div class="job-card">
                    <a href="{{ job.url }}" target="_blank" class="title">{{ job.title }}</a>
                    <div class="meta">🏢 {{ job.company }} | 📍 {{ job.location }}</div>
                    <a href="{{ job.url }}" target="_blank" class="btn">Stelle öffnen</a>
                </div>
                {% endfor %}
            {% else %}
                <div class="empty-state">
                    <h3>Keine Daten in jobs.json gefunden</h3>
                    <p>Die Datei ist entweder leer oder wurde noch nicht von GitHub Actions generiert.</p>
                </div>
            {% endif %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, jobs=jobs, last_update=last_update)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
