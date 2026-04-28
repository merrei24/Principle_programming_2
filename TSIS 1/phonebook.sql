import psycopg2
import json
from datetime import date

# Мәліметтер қорына қосылу (өз деректеріңді жаз)
config = {
    "host": "localhost",
    "database": "phonebook_db",
    "user": "postgres",
    "password": "your_password"
}

def get_connection():
    return psycopg2.connect(**config)

# --- IMPORT / EXPORT LOGIC ---

def export_to_json(filename="contacts.json"):
    conn = get_connection()
    cur = conn.cursor()
    # Реляциялық join арқылы деректерді жинау
    query = """
        SELECT c.first_name, c.email, c.birthday, g.name as group_name,
               ARRAY_AGG(p.phone || ':' || p.type) as phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, g.name
    """
    cur.execute(query)
    rows = cur.fetchall()
    
    data = []
    for r in rows:
        data.append({
            "name": r[0], "email": r[1], 
            "birthday": str(r[2]) if r[2] else None,
            "group": r[3], "phones": r[4]
        })
        
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print("Export successful!")
    cur.close()
    conn.close()

def import_from_json(filename="contacts.json"):
    with open(filename, "r") as f:
        data = json.load(f)
    
    conn = get_connection()
    cur = conn.cursor()
    
    for item in data:
        cur.execute("SELECT id FROM contacts WHERE first_name = %s", (item['name'],))
        exists = cur.fetchone()
        
        if exists:
            choice = input(f"Contact {item['name']} exists. Skip or Overwrite? (s/o): ")
            if choice.lower() == 's': continue
            else: cur.execute("DELETE FROM contacts WHERE first_name = %s", (item['name'],))

        # Жаңа контакт қосу
        cur.execute("INSERT INTO contacts (first_name, email, birthday) VALUES (%s, %s, %s) RETURNING id",
                    (item['name'], item['email'], item['birthday']))
        c_id = cur.fetchone()[0]
        
        # Топқа қосу (процедура арқылы)
        if item.get('group'):
            cur.execute("CALL move_to_group(%s, %s)", (item['name'], item['group']))
            
    conn.commit()
    print("Import finished.")
    cur.close()
    conn.close()

# --- CONSOLE UI & PAGINATION ---

def show_paginated():
    limit = 5
    offset = 0
    while True:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM contacts LIMIT %s OFFSET %s", (limit, offset))
        rows = cur.fetchall()
        
        print("\n--- Contact List ---")
        for r in rows: print(r)
        
        cmd = input("\n[n]ext, [p]rev, [q]uit: ").lower()
        if cmd == 'n': offset += limit
        elif cmd == 'p': offset = max(0, offset - limit)
        elif cmd == 'q': break
        cur.close()
        conn.close()

if __name__ == "__main__":
    # Негізгі мәзірді осында қоссаң болады
    # Мысалы: show_paginated() немесе export_to_json()
    pass