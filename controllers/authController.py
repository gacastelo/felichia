from utils.derivador import derivar_chave
from core.database import Database
import os
import sqlite3
class AuthController:
    def __init__(self):
        self.db = Database()

    def login(self, username, password):
        conn = self.db.get_conn()
        row = conn.execute("SELECT id, senha_hash, salt FROM usuarios WHERE username=?", (username,)).fetchone()
        conn.close()
        if not row:
            print("Usuário não encontrado.")
            return None
        user_id, senha_hash, salt = row
        chave = derivar_chave(password, salt)
        if chave == senha_hash:
            print("Login OK!")
            return user_id, chave
        else:
            print("Senha incorreta.")
            return None

    def cadastro(self, username, password):
        conn = self.db.get_conn()
        salt = os.urandom(16)
        senha_hash = derivar_chave(password, salt)
        try:
            conn.execute("INSERT INTO usuarios (username, senha_hash, salt) VALUES (?, ?, ?)", (username, senha_hash, salt))
            conn.commit()
            print(f"Usuário '{username}' cadastrado com sucesso.")
        except sqlite3.IntegrityError:
            print("Usuário já existe.")
        conn.close()

if __name__ == "__main__":
    opcao = int(input("Digite 1 para cadastro, 2 para login: "))
    db = Database()
    db.setup()
    AuthController = AuthController()
    match opcao:
        case 1:
            AuthController.cadastro("Gabriel", "12345")
        case 2:
            AuthController.login("Gabriel", "12345")