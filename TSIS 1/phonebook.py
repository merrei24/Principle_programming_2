import json
from connect import get_connection
from datetime import date

def show_menu():
    print("\n" + "="*40)
    print("      PHONEBOOK MANAGEMENT SYSTEM")
    print("="*40)
    print("1. View Contacts (Paginated)")
    print("2. Search Contacts (Multi-field)")
    print("3. Export to JSON")
    print("4. Import from JSON (Update Data)")
    print("5. Move Contact to Group")
    print("6. Search by Email")
    print("0. Exit")
    return input("Select an option: ")

# 1. Тізімді көру (Pagination)
def view_contacts():
    limit = 5
    offset = 0
    while True:
        conn = get_connection()
        cur = conn.cursor()
        query = """
            SELECT c.id, c.name, c.email, c.birthday, g.name 
            FROM contacts c 
            LEFT JOIN groups g ON c.group_id = g.id 
            ORDER BY c.name LIMIT %s OFFSET %s
        """
        cur.execute(query, (limit, offset))
        rows = cur.fetchall()
        print(f"\n--- Page (Offset: {offset}) ---")
        if not rows:
            print("No contacts found.")
        
        for r in rows:
            c_id, name, email, bday, g_name = r
            bday_str = bday.strftime('%Y-%m-%d') if bday else "N/A"
            print(f"Name: {name:<12} | Email: {email if email else 'N/A':<20} | Born: {bday_str:<10} | Group: {g_name if g_name else 'None'}")
        
        cmd = input("\n[n]ext, [p]rev, [q]uit: ").lower()
        if cmd == 'n': offset += limit
        elif cmd == 'p': offset = max(0, offset - limit)
        elif cmd == 'q': break
        cur.close(); conn.close()

# 2. Әдемі іздеу (Contact Card форматында)
def search_ui():
    query_str = input("Enter name, email or phone to search: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (query_str,))
    results = cur.fetchall()
    
    print(f"\n🔍 Search Results for '{query_str}':")
    if not results:
        print("No contacts found.")
    else:
        for res in results:
            c_id, name, email, bday, g_name = res
            print(f"{'-'*40}")
            print(f"👤 NAME     : {name}")
            print(f"📧 EMAIL    : {email if email else 'N/A'}")
            print(f"🎂 BIRTHDAY : {bday if bday else 'N/A'}")
            print(f"👥 GROUP    : {g_name if g_name else 'Other'}")
            
            # Телефондарды базадан бөлек алу
            cur.execute("SELECT phone_number, phone_type FROM phones WHERE contact_id = %s", (c_id,))
            phones = cur.fetchall()
            if phones:
                p_list = [f"{p[0]} ({p[1]})" for p in phones]
                print(f"📞 PHONES   : {', '.join(p_list)}")
        print(f"{'-'*40}")
    cur.close(); conn.close()

# 3. Дұрыс экспорт (Ештеңе жоғалмайды)
def export_to_json():
    conn = get_connection()
    cur = conn.cursor()
    query = """
        SELECT c.id, c.name, c.email, c.birthday, g.name 
        FROM contacts c 
        LEFT JOIN groups g ON c.group_id = g.id
    """
    cur.execute(query)
    rows = cur.fetchall()
    
    export_data = []
    for r in rows:
        c_id, name, email, bday, g_name = r
        cur.execute("SELECT phone_number, phone_type FROM phones WHERE contact_id = %s", (c_id,))
        p_rows = cur.fetchall()
        phones = [{"phone": p[0], "type": p[1]} for p in p_rows]
        
        export_data.append({
            "first_name": name,
            "email": email,
            "birthday": str(bday) if bday else None,
            "group": g_name if g_name else "Other",
            "phones": phones
        })
    
    with open("contacts_sample.json", "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=4)
    print("\n[!] Data exported successfully to contacts_sample.json!")
    cur.close(); conn.close()

# 4. Импорт (Деректерді жаңарту)
def import_from_json():
    try:
        with open("contacts_sample.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: contacts_sample.json not found!"); return
    
    conn = get_connection(); cur = conn.cursor()
    for item in data:
        cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (item.get('group', 'Other'),))
        cur.execute("SELECT id FROM groups WHERE name = %s", (item.get('group', 'Other'),))
        group_id = cur.fetchone()[0]

        cur.execute("DELETE FROM contacts WHERE name = %s", (item['first_name'],))
        cur.execute(
            "INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id",
            (item['first_name'], item['email'], item.get('birthday'), group_id)
        )
        contact_id = cur.fetchone()[0]

        if 'phones' in item:
            for p in item['phones']:
                cur.execute("INSERT INTO phones (contact_id, phone_number, phone_type) VALUES (%s, %s, %s)",
                            (contact_id, p['phone'], p['type']))
    conn.commit()
    print("\n[!] Import successful. Database updated!")
    cur.close(); conn.close()

# 6. Email бойынша іздеу
def search_by_email():
    email_query = input("Enter email to search: ")
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT name, email FROM contacts WHERE email ILIKE %s", ('%' + email_query + '%',))
    rows = cur.fetchall()
    if rows:
        for r in rows: print(f"Found: {r[0]} ({r[1]})")
    else: print("No contact found.")
    cur.close(); conn.close()

def main():
    while True:
        choice = show_menu()
        if choice == '1': view_contacts()
        elif choice == '2': search_ui()
        elif choice == '3': export_to_json()
        elif choice == '4': import_from_json()
        elif choice == '5': 
            name = input("Contact name: "); gp = input("New group: ")
            conn = get_connection(); cur = conn.cursor()
            try:
                cur.execute("CALL move_to_group(%s, %s)", (name, gp))
                conn.commit(); print("Moved successfully!")
            except Exception as e: print(f"Error: {e}")
            finally: conn.close()
        elif choice == '6': search_by_email()
        elif choice == '0': break

if __name__ == "__main__":
    main()