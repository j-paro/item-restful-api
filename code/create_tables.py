import sqlite3

from constants import SQLITE_DB_FILE, USER_TABLE_NAME, ITEM_TABLE_NAME

connection = sqlite3.connect(SQLITE_DB_FILE)
cursor = connection.cursor()

#
# Auto-incrementing columns requires "INTEGER".
#
try:
    create_users_table_query = f"""
        CREATE TABLE {USER_TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            username text UNIQUE,
            password text
        )
    """
    cursor.execute(create_users_table_query)
except sqlite3.OperationalError:
    print('Users table already created.')

try:
    create_items_table_query = f"""
        CREATE TABLE {ITEM_TABLE_NAME} (
            name text PRIMARY KEY,
            price real
        )
    """
    cursor.execute(create_items_table_query)
except sqlite3.OperationalError:
    print('Items table already created.')

connection.commit()
connection.close()