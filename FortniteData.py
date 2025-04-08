import sqlite3
import requests
import os
import json

query = "https://fortniteapi.io/v1/loot/list&Authorization:=3d55df55-6683dfb8-a518493e-efb039c4?lang=en"

core_url = "https://fortniteapi.io/v1/loot/list?lang=en"
key = "Authorization:=3d55df55-6683dfb8-a518493e-efb039c4"

""" dir = os.path.dirname(__file__)+ os.sep
conn = sqlite3.connect(dir+'games.sqlite')
cur = conn.cursor()

cur.execute(
    "CREATE TABLE IF NOT EXISTS Fortnite (id INTEGER PRIMARY KEY AUTOINCREMENT, WeaponName TEXT, WeaponDamage INTEGER)"
) """

response = requests.get(query)
data = response.json()
print(data)