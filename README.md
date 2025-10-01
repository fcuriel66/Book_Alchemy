# Book_Alchemy

Simple Flask web app for managing a small book/catalog collection.  
The app uses a JSON-backed data store and includes basic pages and API endpoints for listing, adding, updating, deleting and searching books. Frontend templates are provided under `templates/` and static assets under `static/`.

---

## Quick overview

- Backend: Flask (single-file `app.py`)
- Data storage: JSON file(s) under `data/` (no external DB required)
- Templates: Jinja2 templates under `templates/`
- Static: CSS/JS under `static/`

---

## Repo structure

Book_Alchemy/

├── app.py # Main Flask application (routes + logic)

├── data_models.py # Data model helpers (load/save, helpers)

├── data/ # JSON data files (e.g. books.json)

├── templates/ # Jinja2 templates (index.html, add.html, update.html, ...)

├── static/ # CSS (style.css, etc.)

├── requirements.txt # Python dependencies

└── README.md

---

## Features

- List all books (web page + API)
- Add new book (form + API)
- Edit existing book (form + API)
- Delete book (API)
- Search and/or sort functionality (query parameters)
- Lightweight JSON persistence (easy to inspect and edit)

---

## Requirements

- Python 3.8+
- The packages listed in `requirements.txt` (Flask + helpers)

---

## Install & Run (development)

1. Clone the repository:
   ```bash
   git clone git@github.com:fcuriel66/Book_Alchemy.git
   cd Book_Alchemy
