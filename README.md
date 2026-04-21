# Cities API Coursework Project

## Introduction

This project is a FastAPI-based REST API for global city and country data.
It supports full CRUD operations and includes analytics endpoints for geographic and statistical insights.
### Key Features
- CRUD for `cities`
- CRUD for `countries`
- Analytics endpoints (city count by country, country count by continent)
- Geographic endpoints (cities sorted by latitude, nearest city by city name)
- Works locally and on Render

### Tech Stack
- FastAPI
- SQLAlchemy
- Uvicorn
- MySQL (local fallback)
- PostgreSQL (recommended for Render via `DATABASE_URL`)

---

## API Usage Guide

### 1) Local Run

#### Install dependencies
```bash
pip install -r requirements.txt
```

#### Configure environment variables (recommended: `.env`)
The project supports two database configuration styles:
- Preferred: `DATABASE_URL` (best for PostgreSQL/Render)
- Fallback: `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME` (local MySQL style)

Example `.env`:
```env
DATABASE_URL=
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=weather_api
```

#### Start service
```bash
python -m uvicorn app.main:app --reload
```

#### Access URLs
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health check: `http://127.0.0.1:8000/health`

---

### 2) Run on Render

#### Render Web Service setup
- Build Command:
```bash
pip install -r requirements.txt
```
- Start Command:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### Environment Variables
- `DATABASE_URL`: use the Render PostgreSQL **Internal Database URL** (recommended)

#### Post-deploy checks
- `https://webservice-cw1.onrender.com/health`
- `https://webservice-cw1.onrender.com/docs`

#### Quick API smoke test script
Run the script in the project root to quickly verify key endpoints:
```bash
python smoke_test.py
```

Optional: test local service instead of Render:
```bash
python smoke_test.py --base-url http://127.0.0.1:8000
```

---

## API Documentation

The detailed API documentation:
- PDF version (for assessment submission): `docs/API_Documentation.pdf`

This documentation includes:
- Full endpoint list
- Parameters and response formats
- Example requests and expected responses
- Authentication statement
- Error code reference

You can also use the generated interactive docs:
- Swagger UI: `https://webservice-cw1.onrender.com/docs`
- ReDoc: `https://webservice-cw1.onrender.com/redoc`

---

## Notes

- For Render production, use `DATABASE_URL` with PostgreSQL.
- Local MySQL-style variables are still supported as fallback.
- If CSV import fails, check constraints first (e.g., nullable columns and duplicate primary keys).
- Deployed API base URL: `https://webservice-cw1.onrender.com`

---

## Dataset Source

- Main dataset source: [The Weather Dataset (Kaggle)](https://www.kaggle.com/datasets/guillemservera/global-daily-climate-data)
- Files used in this project:
  - `archive/cities.csv`
  - `archive/countries.csv`

Please follow the dataset license and attribution requirements on the Kaggle page when publishing or sharing derivative work.
