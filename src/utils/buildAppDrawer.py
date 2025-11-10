import flet as ft

def build_app_drawer(page: ft.Page, logout_function):
    def handle_navigation(e):
        drawer_instance = page.views[-1].drawer
        if drawer_instance:
            drawer_instance.open = False
        page.update()
        page.go(e.control.data)

    return ft.NavigationDrawer(
        controls=[
            ft.Container(height=20),
            ft.Container(
                content=ft.Text("Menu", size=25, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ),
            ft.Container(height=10),
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
            ft.ListTile(
                leading=ft.Icon(ft.Icons.LOGOUT),
                title=ft.Text("Sair"),
                data="/logout",
                on_click=handle_navigation
            ),
        ]
    )