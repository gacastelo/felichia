import flet as ft
from zxcvbn import zxcvbn
import string
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from core.database import Database
from core.config import load_settings, save_settings

def check_password_strength(password: str) -> dict:
    if not password:
        return {"score": 0, "strength": "Vazia", "color": ft.Colors.TRANSPARENT, "width_factor": 0}

    result = zxcvbn(password)
    score = result['score']

    if score == 0:
        strength_text = "Muito Fraca"
        color = ft.Colors.RED_500
        width_factor = 0.2
    elif score == 1:
        strength_text = "Fraca"
        color = ft.Colors.ORANGE_500
        width_factor = 0.4
    elif score == 2:
        strength_text = "Média"
        color = ft.Colors.YELLOW_500
        width_factor = 0.6
    elif score == 3:
        strength_text = "Boa"
        color = ft.Colors.LIGHT_GREEN_500
        width_factor = 0.8
    else:  # score 4
        strength_text = "Forte"
        color = ft.Colors.GREEN_500
        width_factor = 1.0

    return {
        "score": score,
        "strength": strength_text,
        "color": color,
        "width_factor": width_factor
    }


def gerar_senha_randomica(tamanho: int, caracteres_especiais: bool) -> str:
    caracteres = string.ascii_letters + string.digits
    if caracteres_especiais:
        caracteres += string.punctuation
    senha = ''.join(secrets.choice(caracteres) for i in range(tamanho))
    return senha

def decrypt(chave, texto_cifrado, nonce) -> str:
    aes = AESGCM(chave)
    senha_plana = aes.decrypt(nonce, texto_cifrado, None).decode()
    return senha_plana

def setup():
    db = Database()
    db.setup()
    load_settings()

def toggle_theme(e):
    page = e.page

    new_theme_mode = ft.ThemeMode.LIGHT if e.control.value else ft.ThemeMode.DARK

    page.theme_mode = new_theme_mode

    page.update()

    settings = load_settings()
    settings["theme"] = "light" if e.control.value else "dark"
    save_settings(settings)