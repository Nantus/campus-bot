import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Створюємо таблицю користувачів, якщо її ще немає"""
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT
                )
            """)

    def set_name(self, user_id, name):
        """Додаємо або оновлюємо ім'я користувача"""
        with self.connection:
            return self.cursor.execute(
                "INSERT OR REPLACE INTO users (user_id, name) VALUES (?, ?)",
                (user_id, name)
            )

    def get_name(self, user_id: int) -> str:
        """Отримуємо ім'я користувача за його ID"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT name FROM users WHERE user_id = ?",
                (user_id,)
            ).fetchone()
            return result[0] if result else "" 


db = Database("users_data.db")