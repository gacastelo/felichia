import os

from core.database import Database

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class NoteController:
    def __init__(self):
        self.db = Database()

    def criar_nota(self, user_id):
        conn = self.db.get_conn()
        cursor = conn.execute("INSERT INTO notas (user_id, titulo) VALUES (?,?)", (user_id, "Nota Sem Título"))
        conn.commit()
        new_note_id = cursor.lastrowid
        conn.close()
        print("Nota salva com sucesso!")
        return new_note_id

    def listar_notas(self, user_id):
        conn = self.db.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, conteudo_cifrado, nonce FROM notas WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        #for titulo, conteudo_cifrado, nonce in rows:
           # conteudo_plano = aes.decrypt(nonce, conteudo_cifrado, None).decode()
           # print(f"Titulo: {titulo}, Conteúdo: {conteudo_plano}")
        return rows

    def excluir_nota(self, user_id, nota_id):
        conn = self.db.get_conn()
        conn.execute("DELETE FROM notas WHERE user_id = ? AND id = ?", (user_id, nota_id))
        conn.commit()
        conn.close()
        print("Nota excluida com sucesso!")

    def editar_nota(self, user_id, chave, nota_id, titulo, conteudo):
        aes = AESGCM(chave)
        nonce = os.urandom(12)
        conteudo_cifrado = aes.encrypt(nonce, conteudo.encode(), None)
        conn = self.db.get_conn()
        conn.execute("UPDATE notas SET titulo = ?, conteudo_cifrado = ?, nonce = ? WHERE user_id = ? AND id = ?", (titulo, conteudo_cifrado, nonce, user_id, nota_id))
        conn.commit()
        conn.close()
        print("Nota editada com sucesso!")

    def buscar_nota_por_id(self, user_id, nota_id):
        conn = self.db.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, conteudo_cifrado, nonce FROM notas WHERE user_id = ? AND id = ?", (user_id, nota_id))
        row = cursor.fetchone()
        conn.close()
        return row