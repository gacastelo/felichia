import flet as ft
from utils.utils import check_password_strength, gerar_senha_randomica, decrypt_password

def build_app_drawer(page: ft.Page):
    def handle_navigation(e):
        drawer_instance = page.views[-1].drawer
        if drawer_instance:
            drawer_instance.open = False
        page.update()
        page.go(e.control.data)

    return ft.NavigationDrawer(
        controls=[
            ft.Container(height=20),

            ft.ListTile(
                leading=ft.Icon(ft.Icons.LOCK_OUTLINE),
                title=ft.Text("Senhas"),
                data="/home",
                on_click=handle_navigation
            ),

            ft.ListTile(
                leading=ft.Icon(ft.Icons.EDIT_NOTE_OUTLINED),
                title=ft.Text("Notas"),
                data="/notas",
                on_click=handle_navigation
            ),

            ft.ListTile(
                leading=ft.Icon(ft.Icons.SETTINGS),
                title=ft.Text("Configurações"),
                data="/config",
                on_click=handle_navigation
            ),
        ]
    )