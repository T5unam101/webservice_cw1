import csv
import os
from pathlib import Path

import pymysql


def parse_float(value: str):
    if value is None:
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    return float(cleaned)


conn = pymysql.connect(
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "weather_api"),
    charset="utf8mb4",
    collation="utf8mb4_unicode_ci",
    use_unicode=True,
    init_command="SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci",
    autocommit=False,
)

sql = """
INSERT INTO countries
(country, native_name, iso2, iso3, population, area, capital, capital_lat, capital_lng, region, continent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
country = VALUES(country),
native_name = VALUES(native_name),
iso3 = VALUES(iso3),
population = VALUES(population),
area = VALUES(area),
capital = VALUES(capital),
capital_lat = VALUES(capital_lat),
capital_lng = VALUES(capital_lng),
region = VALUES(region),
continent = VALUES(continent)
"""

csv_path = Path(__file__).resolve().parent.parent / "archive" / "countries.csv"

try:
    with conn.cursor() as cur:
        cur.execute("SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci")
        with csv_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            next(reader)
            batch = []
            for row in reader:
                batch.append(
                    (
                        row[0],
                        row[1] or None,
                        row[2],
                        row[3],
                        parse_float(row[4]),
                        parse_float(row[5]),
                        row[6] or None,
                        parse_float(row[7]),
                        parse_float(row[8]),
                        row[9] or None,
                        row[10] or None,
                    )
                )
                if len(batch) >= 500:
                    cur.executemany(sql, batch)
                    batch.clear()
            if batch:
                cur.executemany(sql, batch)
    conn.commit()
    print("Countries import finished.")
except Exception as e:
    conn.rollback()
    print("Countries import failed:", repr(e))
finally:
    conn.close()
