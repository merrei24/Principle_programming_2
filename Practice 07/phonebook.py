import psycopg2
import csv

conn = psycopg2.connect(
    dbname="phonebook_db",
    user="postgres",
    password="postgres123",
    host="localhost",
    port="5432"
)

cur = conn.cursor()


def add_contact():
    name = input("Name: ")
    phone = input("Phone: ")
    cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()


def import_csv():
    with open("contacts.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()


def show_contacts():
    cur.execute("SELECT * FROM contacts")
    for row in cur.fetchall():
        print(row)


def search():
    name = input("Search name: ")
    cur.execute("SELECT * FROM contacts WHERE name ILIKE %s", ('%' + name + '%',))
    for row in cur.fetchall():
        print(row)


def update():
    name = input("Name to update: ")
    phone = input("New phone: ")
    cur.execute("UPDATE contacts SET phone=%s WHERE name=%s", (phone, name))
    conn.commit()


def delete():
    value = input("Enter name or phone: ")
    cur.execute("DELETE FROM contacts WHERE name=%s OR phone=%s", (value, value))
    conn.commit()


while True:
    print("\n1.Add\n2.Import CSV\n3.Show\n4.Search\n5.Update\n6.Delete\n7.Exit")
    ch = input("Choose: ")

    if ch == "1":
        add_contact()
    elif ch == "2":
        import_csv()
    elif ch == "3":
        show_contacts()
    elif ch == "4":
        search()
    elif ch == "5":
        update()
    elif ch == "6":
        delete()
    elif ch == "7":
        break
