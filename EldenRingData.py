import sqlite3
import requests
import os
import json

baseUrl = "https://eldenring.fanapis.com/api/weapons?limit=100"


dir = os.path.dirname(__file__)+ os.sep
conn = sqlite3.connect(dir+'games1.sqlite')
cur = conn.cursor()


def createDataset(baseUrl):
    FullDatad = []
    for i in range(0,3, 1):
        URL = baseUrl + "&page=" + str(i)
        resps = requests.get(URL)
        datad = resps.json()
        datad = datad['data']
        FullDatad += datad
    return FullDatad
        



def damage_types(cur, conn):
    cur.execute("SELECT COUNT(Damage_id) FROM DamageTypes")
    current = cur.fetchone()
    current = current[0]
    if(current == 5):
        return
    count = 0
    List = ["Phy", "Mag", "Fire", "Ligt", "Holy"]
    for item in List:
        cur.execute("INSERT OR IGNORE INTO DamageTypes (Damage_id, TypeName) VALUES (?, ?)", (count, item))
        count +=1
    conn.commit()

def weapon_damages(FullData, cur, conn):
    cur.execute("SELECT COUNT(Damage_id) FROM DamageTypes")
    currentTypes = cur.fetchone()
    currentTypes = currentTypes[0]

    cur.execute("SELECT COUNT(Weapon_id) FROM WeaponsDifferentDamages")
    currentDifferent = cur.fetchone()
    currentDifferent = currentDifferent[0]

    if(currentTypes == 0 or currentDifferent == 300):
        return 

    else:
        count = currentDifferent
        for item in FullData[currentDifferent:currentDifferent+25]:
            Physical = item['attack'][0]['amount']
            Magic = item['attack'][1]['amount']
            Fire =  item['attack'][2]['amount']
            Light =  item['attack'][3]['amount']
            Holy =  item['attack'][4]['amount']
            x = max(Physical, Magic, Fire, Light, Holy)
            cur.execute("""INSERT OR IGNORE INTO WeaponsDifferentDamages 
                        (Weapon_id, Physical, Magic, Fire, Light, Holy, MaxDamage) Values 
                        (?, ?, ?, ?, ?, ?, ?)""", 
                        (count, Physical, Magic, Fire, Light, Holy, x))
            count +=1
    conn.commit()


def add_weapons(FullData, cur, conn):
    cur.execute("SELECT COUNT(Weapon_id) FROM WeaponsDifferentDamages")
    currentDifferent = cur.fetchone()
    currentDifferent = currentDifferent[0]

    cur.execute("SELECT COUNT(id) FROM Elden_Ring")
    currentRing = cur.fetchone()
    currentRing = currentRing[0]

    
    if(currentDifferent != 300 or currentRing == 300):
        return 

    else:
        count = currentRing
        for item in FullData[currentRing:currentRing+25]:
            name = item['name']
            #damage = item['attack'][0]['amount']
            Physical = (item['attack'][0]['amount'],item['attack'][0]['name'])
            Magic = (item['attack'][1]['amount'],item['attack'][1]['name'])
            Fire =  (item['attack'][2]['amount'],item['attack'][2]['name'])
            Light =  (item['attack'][3]['amount'],item['attack'][3]['name'])
            Holy =  (item['attack'][4]['amount'],item['attack'][4]['name'])
            x = sorted([Physical, Magic, Fire, Light, Holy], key=lambda t: t[0])
            damageName = x[4][1]
            cur.execute("""SELECT Damage_id FROM DamageTypes WHERE TypeName = ?""",(damageName,))
            damNam = cur.fetchone()
            damNam = damNam[0]
            print(x)
        
            cur.execute("""INSERT OR IGNORE INTO Elden_Ring 
                        (id, WeaponName, MaxDamageType, WeaponDamage) 
                        Values (?,?,?,?)""", 
                        (count, name, damNam,count))
            count += 1
    conn.commit()

cur.execute("CREATE TABLE IF NOT EXISTS Elden_Ring (id INTEGER PRIMARY KEY, WeaponName TEXT, MaxDamageType Text, WeaponDamage Integer)")


cur.execute("CREATE TABLE IF NOT EXISTS WeaponsDifferentDamages (Weapon_id INTEGER PRIMARY KEY, Physical INTEGER, Magic INTEGER, Fire INTEGER, Light INTEGER, Holy Integer, MaxDamage INTEGER)")

cur.execute("CREATE TABLE IF NOT EXISTS DamageTypes (Damage_id INTEGER PRIMARY KEY, TypeName Text)")

FullData = createDataset(baseUrl)
add_weapons(FullData, cur, conn)
weapon_damages(FullData, cur, conn)
damage_types( cur, conn)

