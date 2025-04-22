import requests
import sqlite3

url = "https://mhw-db.com/weapons"

def fetch_mhw_weapon_data(offset=0, limit=25):
    response = requests.get(url)
    if response.status_code == 200:
        full_data = response.json()
        return full_data[offset:offset + limit]
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def connect_db(db_name="mhw_weapons.db"):
    return sqlite3.connect(db_name)

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weapon_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weapons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            attack INTEGER,
            defense INTEGER,
            weapon_type_id INTEGER,
            rarity INTEGER,
            affinity INTEGER,
            damage_type TEXT,
            element_type TEXT,
            element_damage INTEGER,
            elderseal TEXT,
            FOREIGN KEY (weapon_type_id) REFERENCES weapon_types(id)
        )
    ''')
    conn.commit()

def insert_weapon_types(conn, weapon_types):
    cursor = conn.cursor()
    for weapon_type in weapon_types:
        cursor.execute('''
            INSERT OR IGNORE INTO weapon_types (name)
            VALUES (?)''', 
            (weapon_type,)
        )
    conn.commit()

def insert_weapons(conn, weapons):
    cursor = conn.cursor()
    for weapon in weapons:
        cursor.execute('SELECT id FROM weapon_types WHERE name = ?', (weapon["type"],))
        weapon_type_id = cursor.fetchone()
        if weapon_type_id:
            weapon_type_id = weapon_type_id[0]
        else:
            cursor.execute('INSERT INTO weapon_types (name) VALUES (?)', (weapon["type"],))
            weapon_type_id = cursor.lastrowid

        cursor.execute('''
            INSERT OR IGNORE INTO weapons (
                name, attack, defense, weapon_type_id,
                rarity, affinity, damage_type,
                element_type, element_damage, elderseal
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                weapon["name"],
                weapon["attack"],
                weapon["defense"],
                weapon_type_id,
                weapon["rarity"],
                weapon["affinity"],
                weapon["damage_type"],
                weapon["element_type"],
                weapon["element_damage"],
                weapon["elderseal"]
            )
        )
    conn.commit()

def process_and_insert_data(weapon_data, conn):
    weapon_types = set()
    weapons = []

    for weapon in weapon_data:
        attack_info = weapon.get("attack", {})
        attack_value = attack_info.get("display", 0) if isinstance(attack_info, dict) else 0
        defense_value = weapon.get("defense", 0)
        rarity = weapon.get("rarity", 0)
        affinity = weapon.get("affinity", 0)
        damage_type = weapon.get("damageType", None)
        elderseal = weapon.get("elderseal", None)
        element_data = weapon.get("elements", [])
        if element_data and isinstance(element_data, list) and len(element_data) > 0:
            element_type = element_data[0].get("type", None)
            element_damage = element_data[0].get("damage", None)
        else:
            element_type = None
            element_damage = None

        weapon_type = weapon.get("type", "Unknown")
        weapon_types.add(weapon_type)
        weapons.append({
            "name": weapon.get("name", "Unnamed Weapon"),
            "attack": attack_value,
            "defense": defense_value,
            "type": weapon_type,
            "rarity": rarity,
            "affinity": affinity,
            "damage_type": damage_type,
            "element_type": element_type,
            "element_damage": element_damage,
            "elderseal": elderseal
        })

    insert_weapon_types(conn, weapon_types)
    insert_weapons(conn, weapons)
    print(f"Inserted {len(weapons)} weapons into the database.")

def count_weapons_in_db(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM weapons')
    return cursor.fetchone()[0]

if __name__ == "__main__":
    conn = connect_db()
    create_tables(conn)

    offset = 0
    limit = 25

    while True:
        weapon_data = fetch_mhw_weapon_data(offset=offset, limit=limit)
        if not weapon_data:
            print("No more data to fetch. Done!")
            break
        process_and_insert_data(weapon_data, conn)
        offset += limit

    total = count_weapons_in_db(conn)
    print(f"Finished! Total weapons in database: {total}")
    conn.close()
