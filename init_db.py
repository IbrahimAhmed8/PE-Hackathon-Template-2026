import csv
import psycopg2
import os

def seed():
    try:
        conn = psycopg2.connect(
            dbname="hackathon_db",
            user="user",
            password="password",
            host="db",
            port="5432"
        )
        cur = conn.cursor()
        print("[*] Recreating Tables...")
        cur.execute("DROP TABLE IF EXISTS events, urls, users CASCADE;")
        cur.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, email TEXT UNIQUE, created_at TIMESTAMP);")
        cur.execute("CREATE TABLE urls (id SERIAL PRIMARY KEY, user_id INTEGER, short_code TEXT UNIQUE, original_url TEXT, title TEXT, is_active BOOLEAN, created_at TIMESTAMP, updated_at TIMESTAMP);")
        cur.execute("CREATE TABLE events (id SERIAL PRIMARY KEY, url_id INTEGER, user_id INTEGER, event_type TEXT, timestamp TIMESTAMP, details TEXT);")
        
        for file, table in [('users.csv', 'users'), ('urls.csv', 'urls'), ('events.csv', 'events')]:
            if not os.path.exists(file):
                print(f"[!] Warning: {file} not found, skipping...")
                continue
                
            print(f"[*] Seeding {table}...")
            with open(file, 'r') as f:
                reader = csv.DictReader(f)
                cols = reader.fieldnames
                query = f"INSERT INTO {table} ({','.join(cols)}) VALUES ({','.join(['%s'] * len(cols))}) ON CONFLICT DO NOTHING"
                
                for row in reader:
                    if 'is_active' in row:
                        row['is_active'] = str(row['is_active']).lower() == 'true'
                    cur.execute(query, list(row.values()))
        
        conn.commit()
        print("[+] Success: Database Seeded completely!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[-] Seed Error: {e}")

if __name__ == "__main__":
    seed()