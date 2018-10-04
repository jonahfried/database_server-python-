import psycopg2

MILITARY_EQUIPMENT = ["id", "name", "classification", "manID"]
MANUFACTURERS = ["id", "name"]

def get_all_from_ME(cursor):
    cursor.execute("SELECT * FROM militaryEquipment ORDER BY id")
    return [dict(zip(MILITARY_EQUIPMENT, row)) for row in cursor.fetchall()]

def update_from_ME(cursor, equipmentID, name, classification):
    cursor.execute("UPDATE militaryEquipment SET name=%s, classification=%s WHERE id=%s", (name, classification, equipmentID))

def delete_from_ME(cursor, equipmentID):
    cursor.execute("DELETE FROM militaryEquipment WHERE id=%s", (equipmentID,))

def add_to_ME(cursor, name, classification, manufacturer):
    cursor.execute("SELECT id FROM manufacturers WHERE name=%s", (manufacturer,))
    manID = cursor.fetchone()
    if not manID:
        cursor.execute("INSERT INTO manufacturers (id, name) VALUES(default, %s) RETURNING id", (name,))
        manID = cursor.fetchone()
    cursor.execute("INSERT INTO militaryEquipment (id, name, classification, manufacturerID) VALUES(default, %s, %s, %s )", (name, classification, manID[0]))

################################
######## MANUFACTURERS ########
################################
def get_all_from_MAN(cursor):
    cursor.execute("SELECT * FROM manufacturers ORDER BY id")
    return [dict(zip(MANUFACTURERS, row)) for row in cursor.fetchall()]

def update_from_MAN(cursor, manID, name):
    cursor.execute("UPDATE manufacturers SET name=%s WHERE id=%s", (name, manID))

def delete_from_MAN(cursor, manID):
    cursor.execute("DELETE FROM manufacturers WHERE id=%s", (manID,))
    cursor.execute("DELETE FROM militaryEquipment WHERE manufacturerID=%s", (manID,))


def add_to_MAN(cursor, manufacturer):
    cursor.execute("INSERT INTO manufacturers (id, name) VALUES(default, %s)", (manufacturer,))


def reset_databases(cursor):
    cursor.execute("DELETE FROM manufacturers")
    cursor.execute("DELETE FROM militaryEquipment")
    add_to_ME(cursor, "Fokker E IV", "plane", "Fokker")
    add_to_ME(cursor, "Big Plane", "plane", "planesRus")
    add_to_ME(cursor, "little Plane", "plane", "planesRus")
    add_to_ME(cursor, "Blomber Bloi", "bomber", "BombCity")