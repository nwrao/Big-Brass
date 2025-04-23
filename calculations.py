import sqlite3
import os
import matplotlib
import matplotlib.pyplot as plt


dir = os.path.dirname(__file__)+ os.sep
conn = sqlite3.connect(dir+'games1.sqlite')
cur = conn.cursor()


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

def createPieChart(counts):
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
    
def createBarGraph(averages):
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

x = countDamagesElden(cur)
y = averageDamagesElden(cur)
createPieChart(x)
createBarGraph(y)