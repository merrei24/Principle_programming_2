from connect import connect

def search(pattern):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    conn.close()


def add_contact(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()

    conn.close()


def delete_contact(value):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()

    conn.close()


# TEST
if __name__ == "__main__":
    add_contact("Merei", "777")
    search("Merei")
    delete_contact("Merei")