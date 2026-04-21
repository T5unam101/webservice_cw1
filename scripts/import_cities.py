import csv
import pymysql

conn = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="qc04132513",
    database="cities_api",
    charset="utf8mb4",
    collation="utf8mb4_unicode_ci",
    use_unicode=True,
    init_command="SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci",
    autocommit=False,
)

sql = """
INSERT INTO cities
(station_id, city_name, country, state, iso2, iso3, latitude, longitude)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
city_name = VALUES(city_name),
country = VALUES(country),
state = VALUES(state),
iso2 = VALUES(iso2),
iso3 = VALUES(iso3),
latitude = VALUES(latitude),
longitude = VALUES(longitude)
"""

try:
    with conn.cursor() as cur:
        # Double-check session charset to avoid latin-1 client encoding.
        cur.execute("SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci")
        with open(r"E:\web服务cw\archive\cities.csv", "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            batch = []
            row_no = 1
            for row in reader:
                row_no += 1
                batch.append(
                    (
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        float(row[6]),
                        float(row[7]),
                    )
                )
                if len(batch) >= 1000:
                    cur.executemany(sql, batch)
                    batch.clear()
            if batch:
                cur.executemany(sql, batch)
    conn.commit()
    print("Import finished.")
except Exception as e:
    conn.rollback()
    print("Import failed:", repr(e))
finally:
    conn.close()