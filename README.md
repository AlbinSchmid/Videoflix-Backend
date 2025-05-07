# 🎬 Videoflix Backend

Videoflix ist ein leistungsfähiges und skalierbares Backend für eine Video-Streaming-Plattform, entwickelt mit Django, Django REST Framework und PostgreSQL. Es bietet sichere Authentifizierung, Video-Management und Job-Queueing zur optimalen Performance.

--- 

## 🚀 Hauptfeatures

- RESTful API mit Django REST Framework
- Authentifizierung und Autorisierung mit JWT (SimpleJWT)
- Sichere Session-Verwaltung mit HTTP-only Cookies
- Asynchrones Task-Management mit Redis und RQ (inkl. RQ Scheduler)
- Datenbank: PostgreSQL
- CORS-Handling für flexible Frontend-Integration
- Datenimport und -export (CSV, Excel etc.) mit django-import-export
- Umfangreiche Debugging-Tools (Django Debug Toolbar)

---

## 🛠️ Technologie-Stack

- Python 3.11+
- Django 5.1.7
- Django REST Framework 3.16.0
- PostgreSQL
- Redis & RQ
- Gunicorn & Nginx (für Production Deployment)

---

## 📦 Installation

### Voraussetzungen
 
  - Python 3.11+
  - PostgreSQL 
  - Redis

  ### Schritt-für-Schritt Installation

  ```
  # Repository klonen
  git clone git@github.com:AlbinSchmid/Videoflix-Backend.git
  cd videoflix-backend

  # Virtuelle Umgebung einrichten
  python -m venv venv
  source venv/bin/activate

  # Abhängigkeiten installieren
  pip install -r requirements.txt

  # .env-Datei erstellen
  cp .env.example .env
  ```

  ### Umgebungsvariablen konfigurieren

  Bearbeite die .env-Datei mit deinen eigenen Zugangsdaten:

  ```
  DEBUG=True
  SECRET_KEY=dein-geheimer-schlüssel
  DATABASE_URL=postgres://user:password@localhost:5432/videoflix
  REDIS_URL=redis://localhost:6379/0
  ```

  ### Datenbank initialisieren

  ```
  python manage.py migrate
  python manage.py createsuperuser
  ```

  ### Server starten

  ```
  python manage.py runserver
  ```

---

## 🚧 Task Queue starten

```
# Redis starten
redis-server

# RQ Worker starten
python manage.py rqworker default

# RQ Scheduler starten
rqscheduler
```

---

## 🔐 Deployment

Empfohlene Infrastruktur:

- Google Cloud VM
- Nginx (Reverse Proxy mit SSL)
- Gunicorn

--- 

## 🧪 Testing

```
python manage.py test
```

--- 

## ⚙️ Anforderungen (Requirements)

Siehe requirements.txt.

--- 

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

---

## 🙋 Support & Mitwirken

Erstelle gerne Issues oder Pull Requests, um bei der Entwicklung zu helfen oder Fehler zu melden!
