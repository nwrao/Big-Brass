import requests
import sqlite3
import json
import os

url = "https://mhw-db.com/weapons"

def fetch_mhw_weapon_data():
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def connect_db(db_name="Games.db"):
    return sqlite3.connect(db_name)

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mhw_weapon_types (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mhw_weapons (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            attack INTEGER,
            weapon_type_id INTEGER,
            rarity INTEGER,
            damage_type TEXT,
            element_type TEXT,
            element_damage INTEGER,
            elderseal TEXT,
            FOREIGN KEY (weapon_type_id) REFERENCES mhw_weapon_types(id)
        )
    ''')
    conn.commit()

def insert_weapon_types(conn, weapon_types):
    cursor = conn.cursor()
    for weapon_type in weapon_types:
        cursor.execute('''
            INSERT OR IGNORE INTO mhw_weapon_types (name)
            VALUES (?)''', 
            (weapon_type,)
        )
    conn.commit()

def insert_weapons(conn, weapons):
    cursor = conn.cursor()
    inserted_count = 0

    for weapon in weapons:
        cursor.execute('SELECT id FROM mhw_weapons WHERE name = ?', (weapon["name"],))
        if cursor.fetchone():
            continue

        cursor.execute('SELECT id FROM mhw_weapon_types WHERE name = ?', (weapon["type"],))
        weapon_type_id = cursor.fetchone()
        if weapon_type_id:
            weapon_type_id = weapon_type_id[0]
        else:
            cursor.execute('INSERT INTO mhw_weapon_types (name) VALUES (?)', (weapon["type"],))
            weapon_type_id = cursor.lastrowid

        cursor.execute('''
            INSERT INTO mhw_weapons (
                name, attack, weapon_type_id,
                rarity, damage_type,
                element_type, element_damage, elderseal
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                weapon["name"],
                weapon["attack"],
                weapon_type_id,
                weapon["rarity"],
                weapon["damage_type"],
                weapon["element_type"],
                weapon["element_damage"],
                weapon["elderseal"]
            )
        )
        inserted_count += 1

        if inserted_count >= 25:
            break

    conn.commit()
    print(f"Inserted {inserted_count} new weapons into the database.")

def process_and_insert_data(weapon_data, conn):
    weapon_types = []
    weapons = []

    for weapon in weapon_data:
        attack_info = weapon.get("attack", 0)
        if isinstance(attack_info, dict):
            attack_value = attack_info.get("display", 0)
        else:
            attack_value = 0
        rarity = weapon.get("rarity", 0)
        damage_type = weapon.get("damageType", None)
        elderseal = weapon.get("elderseal", None)
        element_data = weapon.get("elements", None)
        if element_data and isinstance(element_data, list) and len(element_data) > 0:
            element_type = element_data[0].get("type", None)
            element_damage = element_data[0].get("damage", None)
        else:
            element_type = None
            element_damage = None

        weapon_type = weapon.get("type", "Unknown")
        weapon_types.append(weapon_type)
        weapons.append({
            "name": weapon.get("name", "Unnamed Weapon"),
            "attack": attack_value,
            "type": weapon_type,
            "rarity": rarity,
            "damage_type": damage_type,
            "element_type": element_type,
            "element_damage": element_damage,
            "elderseal": elderseal
        })

    insert_weapon_types(conn, weapon_types)
    insert_weapons(conn, weapons)

def count_weapons_in_db(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM mhw_weapons')
    return cursor.fetchone()[0]

if __name__ == "__main__":
    conn = connect_db()
    create_tables(conn)

    all_weapon_data = fetch_mhw_weapon_data()
    if all_weapon_data:
        process_and_insert_data(all_weapon_data, conn)

    total = count_weapons_in_db(conn)
    print(f"Finished! Total weapons in database: {total}")
    conn.close()
