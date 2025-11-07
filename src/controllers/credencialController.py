import os

from core.database import Database
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class CredencialController:
    def __init__(self):
        self.db = Database()

    def salvar_credencial(self, user_id, chave, titulo, login, site, senha_plana, tag_id=None):
        aes = AESGCM(chave)
        nonce = os.urandom(12)
        senha_cifrada = aes.encrypt(nonce, senha_plana.encode(), None)
        conn = self.db.get_conn()
        conn.execute(
            "INSERT INTO credenciais (user_id, titulo, login, site, senha_cifrada, nonce, tag_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, titulo, login, site, senha_cifrada, nonce, tag_id))
        conn.commit()
        conn.close()
        print("Credencial salva com sucesso!")

    def listar_credenciais(self, user_id, chave):
        aes = AESGCM(chave)
        conn = self.db.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT titulo, login, site, senha_cifrada, nonce, tag_id FROM credenciais WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        #for titulo, login, site, senha_cifrada, nonce, tag_id in rows:
           # senha_plana = aes.decrypt(nonce, senha_cifrada, None).decode()
           # print(f"Titulo: {titulo}, Login: {login}, Site: {site}, Senha: {senha_plana}")
        return rows


if __name__ == "__main__":
    db = Database()
    db.setup()
    CredencialController = CredencialController()
    CredencialController.salvar_credencial(1, "minha_chave", "Titulo", "Login", "Site", "Senha")

