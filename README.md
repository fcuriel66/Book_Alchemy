# BookOracle
<img width="2020" height="1430" alt="image" src="https://github.com/user-attachments/assets/d864a306-9754-4100-909e-935b678187fd" />


Flask-based Web App for managing a book/catalog collection.  
The app uses a JSON-backed data store and includes pages and API endpoints for listing, adding, updating, deleting and searching for books. As long as a book has a ISBN, the app can search for it and include its inofrmation and its front cover in the generated website. Frontend Jinja2 templates are provided under `templates/` and static assets like and CSS styles are under `static/`.

---

## Quick overview

- Backend: Flask (single-file `app.py`)
- Frontend: HTML/CSS website in Flask server
- Data storage: SQLite file(s) under `data/`. Relational database with Books and Authors tables.
- Templates: Jinja2 templates under `templates/`
- Static: CSS/JS under `static/`

---

## Repo structure

Book_Alchemy/
```
├── app.py # Main Flask application (routes + logic)
├── data_models.py # Data model helpers (load/save, helpers)
├── data/ # SQLite data files (Relational DB)
├── templates/ # Jinja2 templates (index.html, add.html, update.html, ...)
├── static/ # CSS (style.css, etc.)
├── requirements.txt # Python dependencies
└── README.md
```
---

## Features

- List all books (web page + API)
- Add new book (form + API)
- Edit existing book (form)
- Delete book (form)
- Search and/or sort functionality (in Homepage)
- SQLite data persistence (easy to inspect and edit)

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
