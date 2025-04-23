import sqlite3
import os
import matplotlib
import matplotlib.pyplot as plt

dir = os.path.dirname(__file__) + os.sep
conn = sqlite3.connect(dir + "Games.sqlite")
cur = conn.cursor()

def countTypesMHW(cur):
    cur.execute('''
        SELECT wt.name, COUNT(w.id)
        FROM mhw_weapons w
        JOIN mhw_weapon_types wt ON w.weapon_type_id = wt.id
        GROUP BY w.weapon_type_id
    ''')
    results = cur.fetchall()
    return results

def createPieChart(results):
    labels = []
    counts = []
    for item in results:
        labels.append(item[0])
        counts.append(item[1])

    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=170)
    plt.title("Distribution of MHW Weapons by Type")
    plt.axis('equal')
    plt.show()

def averageDamagesMHW(cur):
    cur.execute('''
        SELECT wt.name, AVG(w.attack)
        FROM mhw_weapons w
        JOIN mhw_weapon_types wt ON w.weapon_type_id = wt.id
        GROUP BY w.weapon_type_id
    ''')
    results = cur.fetchall()
    return results

def createBarChart(results):
    types = []
    averages = []
    for item in results:
        types.append(item[0])
        averages.append(item[1])
    
    plt.figure(figsize=(10, 6))
    plt.barh(types, averages, color='orange')
    plt.xlabel("Average Attack Power")
    plt.title("Average Attack Power by MHW Weapon Type")
    plt.tight_layout()
    plt.show()

type_counts = countTypesMHW(cur)
createPieChart(type_counts)
avg_attack = averageDamagesMHW(cur)
createBarChart(avg_attack)
