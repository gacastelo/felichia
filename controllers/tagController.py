from core.database import Database
class TagController:
    def __init__(self):
        self.db = Database()

    def salvar_tag(self, user_id, title):
        conn = self.db.get_conn()
        conn.execute("INSERT INTO Tags (user_id, title) VALUES (?, ?)", (user_id, title))
        conn.commit()
        conn.close()
        print("Tag salva com sucesso!")

    def listar_tags(self, user_id):
        conn = self.db.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM Tags WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        for title in rows:
            print(title)
        return rows

    def deletar_tag(self, tag_id):
        conn = self.db.get_conn()
        conn.execute("DELETE FROM Tags WHERE id = ?", (tag_id,))
        conn.commit()
        conn.close()
        print("Tag deletada com sucesso!")

    def get_by_id(self, tag_id):
        conn = self.db.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM Tags WHERE id = ?", (tag_id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def get_by_title(self, title):
        conn = self.db.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Tags WHERE title = ?", (title,))
        row = cursor.fetchone()
        conn.close()
        return row