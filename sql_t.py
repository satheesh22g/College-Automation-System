import sqlite3

DB_PATH = "database.db"  # adjust path if needed

def read_all_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("""
        SELECT * from accounts;
    """)
    tables = cursor.fetchall()
    print(tables)
    if not tables:
        print("No tables found in database.")
        return

    # for (table_name,) in tables:
    #     print("\n" + "=" * 60)
    #     print(f"TABLE: {table_name}")
    #     print("=" * 60)

    #     # Get column names
    #     cursor.execute(f"PRAGMA table_info({table_name});")
    #     columns = [col[1] for col in cursor.fetchall()]
    #     print("Columns:", columns)

    #     # Get table data
    #     cursor.execute(f"SELECT * FROM {table_name};")
    #     rows = cursor.fetchall()

    #     if not rows:
    #         print("No data found.")
    #     else:
    #         for row in rows:
    #             print(row)

    conn.close()

if __name__ == "__main__":
    read_all_tables(DB_PATH)
