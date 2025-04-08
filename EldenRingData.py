import sqlite3
import requests
import os
import json

url = "https://eldenring.fanapis.com/api/items?limit=100"

dir = os.path.dirname(__file__)+ os.sep
conn = sqlite3.connect(dir+'games.sqlite')
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS Elden_Ring (id INTEGER PRIMARY KEY AUTOINCREMENT, WeaponName TEXT, WeaponDamage Integer)")

resp = requests.get(url)
data = resp.json

print(data["name"])

