import sqlite3

from constants import SQLITE_DB_FILE, ITEM_TABLE_NAME


class ItemExistsError(sqlite3.IntegrityError):
    pass


class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price


    def to_json(self):
        return {'name': self.name, 'price': self.price}


    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect(SQLITE_DB_FILE)
        cursor = connection.cursor()

        query = f"SELECT * FROM {ITEM_TABLE_NAME} WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(row[0], row[1])


    @classmethod
    def select(cls, name):
        connection = sqlite3.connect(SQLITE_DB_FILE)
        cursor = connection.cursor()

        get_item_query = f"""
            SELECT * FROM {ITEM_TABLE_NAME} WHERE name=?
        """
        result = cursor.execute(get_item_query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(row[0], row[1])


    @classmethod
    def get_all_items(cls):
        connection = sqlite3.connect(SQLITE_DB_FILE)
        cursor = connection.cursor()

        get_items_query = f"""
            SELECT * FROM {ITEM_TABLE_NAME}
        """
        result = cursor.execute(get_items_query)
        items = []

        for row in result:
            items.append(cls(row[0], row[1]))

        connection.commit()
        connection.close()

        return items


    def insert(self):
        connection = sqlite3.connect(SQLITE_DB_FILE)
        cursor = connection.cursor()

        try:
            insert_item_query = f"""
                INSERT INTO {ITEM_TABLE_NAME} VALUES(?, ?)
            """
            cursor.execute(insert_item_query, (self.name, self.price))
        except sqlite3.IntegrityError as e:
            connection.close()
            print(e.__str__())
            print(e.__repr__())
            raise ItemExistsError
        
        connection.commit()
        connection.close()


    def update(self, price):
        connection = sqlite3.connect(SQLITE_DB_FILE)
        cursor = connection.cursor()

        item_modify_query = f"""
            UPDATE {ITEM_TABLE_NAME}
            SET price=?
            WHERE name=?
        """
        cursor.execute(item_modify_query, (price, self.name))

        connection.commit()
        connection.close()


    def delete(self):
        connection = sqlite3.connect(SQLITE_DB_FILE)
        cursor = connection.cursor()

        delete_item_query = f"""
            DELETE FROM {ITEM_TABLE_NAME} WHERE name=?
        """
        cursor.execute(delete_item_query, (self.name,))

        connection.commit()
        connection.close()