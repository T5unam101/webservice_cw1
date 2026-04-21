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
- `https://<your-render-domain>/health`
- `https://<your-render-domain>/docs`

---

## API Reference: Purpose, Example Call, Example Response

Notes:
- All responses are JSON, except `204 No Content`.
- Replace `http://127.0.0.1:8000` with your Render domain in production.

### Health

#### `GET /health`
Purpose: service health check.

```bash
curl http://127.0.0.1:8000/health
```

```json
{
  "status": "ok"
}
```

---

## Cities Endpoints

#### `POST /cities`
Purpose: create a city record.

```bash
curl -X POST http://127.0.0.1:8000/cities \
  -H "Content-Type: application/json" \
  -d '{
    "station_id":"T001",
    "city_name":"Test City",
    "country":"Testland",
    "state":"Test State",
    "iso2":"TT",
    "iso3":"TST",
    "latitude":10.1234567,
    "longitude":20.1234567
  }'
```

```json
{
  "station_id": "T001",
  "city_name": "Test City",
  "country": "Testland",
  "state": "Test State",
  "iso2": "TT",
  "iso3": "TST",
  "latitude": 10.1234567,
  "longitude": 20.1234567
}
```

#### `GET /cities`
Purpose: list cities with pagination.

```bash
curl "http://127.0.0.1:8000/cities?skip=0&limit=5"
```

#### `GET /cities/by-latitude`
Purpose: list cities sorted by latitude descending (closer to North Pole first).

```bash
curl "http://127.0.0.1:8000/cities/by-latitude?limit=10"
```

#### `GET /cities/nearest`
Purpose: find the nearest city to a given city name (`iso2` optional for disambiguation).

```bash
curl "http://127.0.0.1:8000/cities/nearest?city_name=London&iso2=GB"
```

```json
{
  "query": { "city_name": "London", "iso2": "GB" },
  "source_city": {
    "station_id": "03772",
    "city_name": "London",
    "country": "United Kingdom",
    "state": "England",
    "iso2": "GB",
    "iso3": "GBR",
    "latitude": 51.5072222,
    "longitude": -0.1275
  },
  "nearest_city": {
    "station_id": "XXXXX",
    "city_name": "Nearby City",
    "country": "United Kingdom",
    "state": "England",
    "iso2": "GB",
    "iso3": "GBR",
    "latitude": 51.4,
    "longitude": -0.2
  },
  "distance_km": 12.345
}
```

#### `GET /cities/{station_id}`
Purpose: get a city by station ID.

```bash
curl http://127.0.0.1:8000/cities/41515
```

#### `PUT /cities/{station_id}`
Purpose: update a city by station ID.

```bash
curl -X PUT http://127.0.0.1:8000/cities/41515 \
  -H "Content-Type: application/json" \
  -d '{
    "city_name":"Asadabad",
    "country":"Afghanistan",
    "state":"Updated State",
    "iso2":"AF",
    "iso3":"AFG",
    "latitude":34.866,
    "longitude":71.150
  }'
```

#### `DELETE /cities/{station_id}`
Purpose: delete a city by station ID.

```bash
curl -X DELETE http://127.0.0.1:8000/cities/41515
```

---

## Countries Endpoints

#### `POST /countries`
Purpose: create a country record.

```bash
curl -X POST http://127.0.0.1:8000/countries \
  -H "Content-Type: application/json" \
  -d '{
    "iso2":"TS",
    "country":"Testonia",
    "native_name":"Testonia",
    "iso3":"TST",
    "population":1000000,
    "area":12345,
    "capital":"Test City",
    "capital_lat":10.1,
    "capital_lng":20.2,
    "region":"Test Region",
    "continent":"Asia"
  }'
```

#### `GET /countries`
Purpose: list countries with pagination and optional continent filter.

```bash
curl "http://127.0.0.1:8000/countries?skip=0&limit=10&continent=Asia"
```

#### `GET /countries/{iso2}`
Purpose: get a country by ISO2 code.

```bash
curl http://127.0.0.1:8000/countries/AF
```

#### `PUT /countries/{iso2}`
Purpose: update a country by ISO2 code.

```bash
curl -X PUT http://127.0.0.1:8000/countries/AF \
  -H "Content-Type: application/json" \
  -d '{
    "country":"Afghanistan",
    "native_name":"افغانستان",
    "iso3":"AFG",
    "population":26023100,
    "area":652230,
    "capital":"Kabul",
    "capital_lat":34.526011,
    "capital_lng":69.177684,
    "region":"Southern and Central Asia",
    "continent":"Asia"
  }'
```

#### `DELETE /countries/{iso2}`
Purpose: delete a country by ISO2 code.

```bash
curl -X DELETE http://127.0.0.1:8000/countries/AF
```

---

## Analytics Endpoints

#### `GET /analytics/cities-per-country`
Purpose: count cities per country and return results in descending order.

```bash
curl "http://127.0.0.1:8000/analytics/cities-per-country?limit=10"
```

#### `GET /analytics/countries-by-continent`
Purpose: count countries by continent.

```bash
curl "http://127.0.0.1:8000/analytics/countries-by-continent"
```

---

## Notes

- For Render production, use `DATABASE_URL` with PostgreSQL.
- Local MySQL-style variables are still supported as fallback.
- If CSV import fails, check constraints first (e.g., nullable columns and duplicate primary keys).

---

## Dataset Source

- Main dataset source: [The Weather Dataset (Kaggle)](https://www.kaggle.com/datasets/guillemservera/global-daily-climate-data)
- Files used in this project:
  - `archive/cities.csv`
  - `archive/countries.csv`

Please follow the dataset license and attribution requirements on the Kaggle page when publishing or sharing derivative work.
