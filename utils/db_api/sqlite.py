import sqlite3

class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        #izohcha: Jadval endi mavjud bo‘lmasa yaratiladi, id AUTOINCREMENT, tg_id noyob
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER UNIQUE,
            fullname TEXT
        );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, tg_id: int, fullname: str):
        #izohcha: Foydalanuvchi mavjud bo‘lsa, qayta qo‘shmaydi
        sql = """
        INSERT OR IGNORE INTO Users(tg_id, fullname) VALUES(?, ?)
        """
        self.execute(sql, parameters=(tg_id, fullname), commit=True)

    def select_id_users(self):
        sql = """
        SELECT id FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        #izohcha: mos keluvchi foydalanuvchini topadi
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        #izohcha: foydalanuvchilar sonini qaytaradi
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user(self, tg_id: int, fullname: str):
        #izohcha: foydalanuvchining ismini yangilaydi
        sql = """
        UPDATE Users SET fullname = ? WHERE tg_id = ?
        """
        self.execute(sql, parameters=(fullname, tg_id), commit=True)

    def delete_users(self):
        #izohcha: barcha foydalanuvchilarni o‘chiradi
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
