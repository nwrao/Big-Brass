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


def countDamagesElden(cur):
    d = {}
    for i in range(0,5,1):
        cur.execute("""SELECT Elden_Ring.MaxDamageType, DamageTypes.TypeName FROM Elden_Ring JOIN DamageTypes ON Elden_Ring.MaxDamageType = DamageTypes.Damage_id WHERE Elden_Ring.MaxDamageType = ? """, (i,))
        result = cur.fetchall()
        length = len(result)
        if length == 0:
            cur.execute("""SELECT TypeName FROM DamageTypes WHERE Damage_id = ?""", (i,))
            results = cur.fetchone()
            key = results[0]
            value = 0
            d[key] = value
            
        else:

            key = result[0][1]
            value = length
            d[key]=value

    sorted_d = sorted(d.items(), key = lambda x:x[1], reverse = True)
    return sorted_d

def createPieChartElden(counts):
    names = []
    vals = []
    for item in counts:
        names.append(item[0])
        vals.append(item[1])
    colors = ['orange', 'yellow', 'purple', 'red', 'grey'] 
    fig, ax = plt.subplots()
    ax.pie(vals, labels= names, autopct='%1.1f%%', colors=colors[:5])

    plt.title("Number of Elden Ring Weapons With a Specific Damage Type")
    plt.show()



def averageDamagesElden(cur):
    d = {}
    cur.execute("""SELECT WeaponsDifferentDamages.MaxDamage, DamageTypes.TypeName FROM 
                WeaponsDifferentDamages JOIN Elden_Ring ON WeaponsDifferentDamages.Weapon_id = Elden_Ring.WeaponDamage
                JOIN DamageTypes ON Elden_Ring.MaxDamageType = DamageTypes.Damage_id""")
    results = cur.fetchall()
    typenames = ['Phy', 'Mag', 'Fire', 'Ligt', 'Holy']
    for item in typenames:
        sum = 0
        count = 0
        for items in results:
            
            if items[1] == item:
                sum += items[0]
                count += 1
        if sum == 0:
            key = item
            value = 0
            d[key]=value
        else:

            averageVal = sum/count
            d[item] = averageVal

    sorted_d = sorted(d.items(), key = lambda x:x[1], reverse = True)
    return sorted_d
    
def createBarGraphElden(averages):
    names = []
    vals = []
    for item in averages:
        names.append(item[1])
        vals.append(item[0])
    colors = ['orange', 'red', 'yellow', 'purple', 'grey'] 
    fig, ax = plt.subplots()
    ax.barh(vals, names, color=colors[:5])

    plt.title("Average Damage per Weapon Type in Elden Ring")
    plt.xlabel("Total Damage")
    plt.ylabel("Damage Types")
    plt.show()

def creatBarBoth(ave1, ave2):
    names = []
    vals = []
    for item in ave1:
        names.append(item[1])
        vals.append(item[0])
    for item in ave2:
        vals.append(item[0])
        names.append(item[1])
            
    plt.figure(figsize=(10, 6))
    plt.barh(vals, names, color='Pink')
    plt.xlabel("Average Attack Power or Damage")
    plt.ylabel("Weapon or Damage Types")
    plt.title("Average Attack Power between both APIs")
    plt.tight_layout()
    plt.show()

def writeToFile(cur):
    path = os.path.join(dir, "calculations.txt")
    with open(path, "w") as f:
        f.write("Calculation Summary\n")
        f.write("============================\n\n")

        f.write("Calculation 1: MHW Weapon Type Distribution\n")
        f.write("--------------------------------\n")
        f.write("Counts how many weapons exist for each weapon type in Monster Hunter World.\n\n")
        cur.execute('''
            SELECT wt.name, COUNT(w.id)
            FROM mhw_weapons w
            JOIN mhw_weapon_types wt ON w.weapon_type_id = wt.id
            GROUP BY w.weapon_type_id
        ''')
        mhw_counts = cur.fetchall()
        for wt, count in mhw_counts:
            f.write(f"- {wt}: {count} weapons\n")


        f.write("\nCalculation 2:MHW Average Attack by Weapon Type\n")
        f.write("------------------------------------\n")
        f.write("Calculates the average attack power of weapons in each weapon class in Monster Hunter World.\n\n")
        cur.execute('''
            SELECT wt.name, AVG(w.attack)
            FROM mhw_weapons w
            JOIN mhw_weapon_types wt ON w.weapon_type_id = wt.id
            GROUP BY w.weapon_type_id
        ''')
        mhw_avg = cur.fetchall()
        for wt, avg in mhw_avg:
            f.write(f"- {wt}: {avg:.2f} average attack\n")


        f.write("\Calculation 3:. Elden Ring Weapon Damage Type Distribution\n")
        f.write("---------------------------------------------\n")
        f.write("Counts how many weapons use each primary damage type in Elden Ring.\n\n")
        damage_types = ['Phy', 'Mag', 'Fire', 'Ligt', 'Holy']
        damage_count = countDamagesElden(cur)
        for dmg in damage_count:
            f.write(f"- {dmg[0]}: {dmg[1]} weapons\n")

        
        f.write("\Calculation 4: Elden Ring Average Damage by Type\n")
        f.write("------------------------------------\n")
        f.write("Computes the average maximum damage value per damage type in Elden Ring.\n\n")
        avg_dmg = averageDamagesElden(cur)
        for val, typ in avg_dmg:
            f.write(f"- {typ}: {val:.2f} average damage\n")

        f.write("\nCalculation 5: Average Attack Powers Between Games\n")
        f.write("------------------------------------\n")
        f.write("Compares average weapon damage types from Elden Ring with average attack powers from Monster Hunter World.\n\n")
        f.write("Elden Ring Averages:\n")
        for val, typ in avg_dmg:
            f.write(f"- {typ}: {val:.2f} average damage\n")
        f.write("\nMonster Hunter World Averages:\n")
        for wt, avg in mhw_avg:
            f.write(f"- {wt}: {avg:.2f} average attack\n")

x = countDamagesElden(cur)
y = averageDamagesElden(cur)
createPieChartElden(x)
createBarGraphElden(y)
type_counts = countTypesMHW(cur)
createPieChart(type_counts)
avg_attack = averageDamagesMHW(cur)
createBarChart(avg_attack)
creatBarBoth(y, avg_attack)

writeToFile(cur)