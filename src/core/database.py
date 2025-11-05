import os
import sqlite3

class Database:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(base_dir, "..", "..")

        self.db_path = os.path.join(project_root, "storage", "data", "database.db")

        print(f"Caminho do DB: {self.db_path}")

    def get_conn(self):
        return sqlite3.connect(self.db_path)

    def setup(self):
        conn = self.get_conn()

        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            senha_hash BLOB NOT NULL,
            salt BLOB NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES usuarios(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS credenciais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            login TEXT NOT NULL,
            site TEXT NOT NULL,
            senha_cifrada BLOB NOT NULL,
            nonce BLOB NOT NULL UNIQUE,
            tag_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY(tag_id)  REFERENCES Tags(id)  ON DELETE SET NULL
        );
        """)
        conn.commit()


if __name__ == "__main__":
    db = Database()
    db.setup()