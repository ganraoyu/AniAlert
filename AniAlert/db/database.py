import sqlite3
import json

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("""
  CREATE TABLE IF NOT EXISTS anime_notify_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER NOT NULL,
    guild_name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    user_name TEXT NOT NULL,
    anime_name TEXT NOT NULL,
    episode INTEGER,
    unix_air_time INTEGER,
    iso_air_time TEXT,
    image TEXT, 
    episodes_list TEXT
  );
""")

conn.commit()

if __name__ == '__main__':
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
  tables = cursor.fetchall()
  print("Tables:", tables) 

  cursor.execute("SELECT * FROM anime_notify_list;")
  rows = cursor.fetchall()

  print("Rows in anime_notify_list:")
  for row in rows:
      print(json.dumps({
          "guild_id": row[1],
          "guild_name": row[2],
          "user_id": row[3],
          "user_name": row[4],
          "anime_name": row[5],
          "episode": row[6],
          "unix_air_time": row[7],
          "iso_air_time": row[8],
          "image": row[9],
          "episodes_list": json.loads(row[10]) if row[10] else []
      }, indent=2, ensure_ascii=False))

  conn.close()
