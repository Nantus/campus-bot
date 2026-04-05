import sqlite3


class Database:
    def __init__(self, db_file: str):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT
                )
            """)

    def set_name(self, user_id: int, name: str):
        with self.connection:
            return self.cursor.execute(
                "INSERT OR REPLACE INTO users (user_id, name) VALUES (?, ?)",
                (user_id, name)
            )

    def get_name(self, user_id: int) -> str:
        with self.connection:
            result = self.cursor.execute(
                "SELECT name FROM users WHERE user_id = ?",
                (user_id,)
            ).fetchone()
            return result[0] if result else "" 
    
    def get_all_users(self):
        with self.connection:
            result = self.cursor.execute("SELECT user_id FROM users").fetchall()
            return [row[0] for row in result]


db = Database("users_data.db")