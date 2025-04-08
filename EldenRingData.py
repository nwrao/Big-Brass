import sqlite3
import requests
import os
import json


url = "https://eldenring.fanapis.com/api/weapons?limit=300"
url2 = "https://eldenring.fanapis.com/api/weapons?limit=100&page=1"
url3 = "https://eldenring.fanapis.com/api/weapons?limit=100&page=2"

dir = os.path.dirname(__file__)+ os.sep
conn = sqlite3.connect(dir+'games.sqlite')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS Elden_Ring")
cur.execute("CREATE TABLE IF NOT EXISTS Elden_Ring (id INTEGER PRIMARY KEY, WeaponName TEXT, WeaponDamage Integer)")

resp = requests.get(url)
resp2 = requests.get(url2)
resp3 = requests.get(url3)

data = resp.json()
data2 = resp2.json()
data3 = resp3.json()

data = data['data']
data2 = data2['data']
data3= data3['data']


cur.execute("CREATE TABLE IF NOT EXISTS WeaponsDifferentDamages (Weapon_id INTEGER PRIMARY KEY, Physical INTEGER, Magic INTEGER, Fire INTEGER, Light INTEGER, Holy Integer, MaxDamage INTEGER)")


def weapon_damages(data,data2, data3, cur, conn):
    count = 0
    for item in data:
        Physical = item['attack'][0]['amount']
        Magic = item['attack'][1]['amount']
        Fire =  item['attack'][2]['amount']
        Light =  item['attack'][3]['amount']
        Holy =  item['attack'][4]['amount']
        x = max(Physical, Magic, Fire, Light, Holy)
        cur.execute("INSERT OR IGNORE INTO WeaponsDifferentDamages (Weapon_id, Physical, Magic, Fire, Light, Holy, MaxDamage) Values (?, ?, ?, ?, ?, ?, ?)", (count, Physical, Magic, Fire, Light, Holy, x))
        count +=1
    for item in data2:
        Physical = item['attack'][0]['amount']
        Magic = item['attack'][1]['amount']
        Fire =  item['attack'][2]['amount']
        Light =  item['attack'][3]['amount']
        Holy =  item['attack'][4]['amount']
        x = max(Physical, Magic, Fire, Light, Holy)
        cur.execute("INSERT OR IGNORE INTO WeaponsDifferentDamages (Weapon_id, Physical, Magic, Fire, Light, Holy, MaxDamage) Values (?, ?, ?, ?, ?, ?, ?)", (count, Physical, Magic, Fire, Light, Holy, x))
        count +=1
    for item in data3:
        Physical = item['attack'][0]['amount']
        Magic = item['attack'][1]['amount']
        Fire =  item['attack'][2]['amount']
        Light =  item['attack'][3]['amount']
        Holy =  item['attack'][4]['amount']
        x = max(Physical, Magic, Fire, Light, Holy)
        cur.execute("INSERT OR IGNORE INTO WeaponsDifferentDamages (Weapon_id, Physical, Magic, Fire, Light, Holy, MaxDamage) Values (?, ?, ?, ?, ?, ?, ?)", (count, Physical, Magic, Fire, Light, Holy, x))
        count +=1
    conn.commit()

def add_weapons(data,data2, data3, cur, conn):
    count = 0
    for item in data:
        name = item['name']
        #damage = item['attack'][0]['amount']
        cur.execute("INSERT OR IGNORE INTO Elden_Ring (id, WeaponName, WeaponDamage) Values (?,?,?)", (count, name, count))
        count +=1
    for item in data2:
        name = item['name']
        #damage = item['attack'][0]['amount']
        cur.execute("INSERT OR IGNORE INTO Elden_Ring (id, WeaponName, WeaponDamage) Values (?,?,?)", (count, name, count))
        count +=1
    for item in data3:
        name = item['name']
        #damage = item['attack'][0]['amount']
        cur.execute("INSERT OR IGNORE INTO Elden_Ring (id, WeaponName, WeaponDamage) Values (?,?,?)", (count, name, count))
        count +=1
    
    conn.commit()


#print(data['name'])
weapon_damages(data, data2, data3, cur, conn)
add_weapons(data, data2, data3, cur, conn)



