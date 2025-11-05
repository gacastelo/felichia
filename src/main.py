import flet as ft
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from core.database import Database
from controllers.authController import AuthController
from controllers.tagController import TagController
from controllers.credencialController import CredencialController


def setup():
    db = Database()
    db.setup()


def build_app_drawer(page: ft.Page):


    def handle_navigation(e):
        page.go(e.control.data)
        page.update()

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

def main(page: ft.Page):
    setup()
    auth_controller = AuthController()
    page.title = "Felichia"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    def create_login_view():
        page.title = "Felichia - Login"

        username_field = ft.TextField(label="Username", width=300, icon=ft.Icons.PERSON_OUTLINE)
        senha_field = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300,
                                   icon=ft.Icons.LOCK_OUTLINE)

        def handle_login(e):
            if username_field.value and senha_field.value:
                status, user_id, chave = auth_controller.login(username_field.value, senha_field.value)
                if status == "Senha incorreta.":
                    page.open(ft.SnackBar(ft.Text(status, weight=ft.FontWeight.BOLD), bgcolor="#a9a1f9"))
                page.update()
                if user_id and chave:
                    page.go("/home")
            else:
                page.open(
                    ft.SnackBar(ft.Text("Preencha todos os campos!", weight=ft.FontWeight.BOLD), bgcolor="#a9a1f9"))
                page.update()

        return ft.View(
            route="/",
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Acesse sua Conta", size=24, weight=ft.FontWeight.BOLD),
                            username_field,
                            senha_field,
                            ft.ElevatedButton(
                                text="ENTRAR",
                                on_click=handle_login,
                                width=300,
                                style=ft.ButtonStyle(bgcolor="#544E9E", color=ft.Colors.WHITE)
                            ),
                            ft.TextButton(
                                text="Não tem uma conta? Cadastre-se",
                                on_click=lambda _: page.go("/register")
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15
                    ),
                    padding=20,
                    border_radius=10,
                    width=400,
                    alignment=ft.alignment.center
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def create_register_view():
        page.title = "Felichia - Cadastro"

        username_field = ft.TextField(label="Criar Username", width=300, icon=ft.Icons.PERSON_OUTLINE)
        senha_field = ft.TextField(label="Criar Senha", password=True, can_reveal_password=True, width=300,
                                   icon=ft.Icons.LOCK_OUTLINE)

        def handle_register(e):
            if username_field.value and senha_field.value:
                status = auth_controller.cadastro(username_field.value, senha_field.value)
                page.open(ft.SnackBar(ft.Text(status, weight=ft.FontWeight.BOLD), bgcolor="#a9a1f9"))
                page.go("/")
            else:
                page.open(ft.SnackBar(ft.Text("Preencha todos os campos do cadastro!", weight=ft.FontWeight.BOLD),
                                      bgcolor="#a9a1f9"))

            page.update()

        return ft.View(
            route="/register",
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Crie sua Conta", size=24, weight=ft.FontWeight.BOLD),
                            username_field,
                            senha_field,
                            ft.ElevatedButton(
                                text="CADASTRAR",
                                on_click=handle_register,
                                width=300,
                                style=ft.ButtonStyle(bgcolor="#544E9E", color=ft.Colors.WHITE)
                            ),
                            ft.TextButton(
                                text="Já tenho uma conta. Voltar para Login",
                                on_click=lambda _: page.go("/")
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15
                    ),
                    padding=20,
                    border_radius=10,
                    width=400,
                    alignment=ft.alignment.center
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def create_home_view():
        page.title = "Felichia - Minhas Senhas"

        drawer = build_app_drawer(page)

        def button_click(e):
            print("Botão de Ajuda Clicado!")
            page.update()

        main_content = ft.Column(
            [
                ft.Text("Home", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Seu conteúdo e listas virão aqui..."),
                ft.Container(height=300),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True
        )

        floating_button_container = ft.Container(
            content=ft.ElevatedButton(
                content=ft.Icon(ft.Icons.ADD),
                on_click=button_click,
                style=ft.ButtonStyle(
                    shape=ft.CircleBorder(),
                    padding=ft.padding.all(25),
                    bgcolor="#a9a1f9",
                    color=ft.Colors.WHITE
                ),
            ),
            right=20,
            bottom=20,
        )

        stack_layout = ft.Stack(
            [
                main_content,
                floating_button_container
            ],
            expand=True
        )

        return ft.View(
            route="/home",
            controls=[
                ft.AppBar(
                    title=ft.Text("Minhas Senhas"),
                    bgcolor="#544E9E",
                ),
                stack_layout
            ],
            drawer=drawer,
        )

    def create_notas_view():
        page.title = "Felichia - Minhas Notas"

        drawer = build_app_drawer(page)

        def button_click(e):
            print("Botão de Ajuda Clicado!")
            page.update()

        main_content = ft.Column(
            [
                ft.Text("Minhas Notas", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Seu conteúdo e listas virão aqui..."),
                ft.Container(height=300),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True
        )

        floating_button_container = ft.Container(
            content=ft.ElevatedButton(
                content=ft.Icon(ft.Icons.ADD),
                on_click=button_click,
                style=ft.ButtonStyle(
                    shape=ft.CircleBorder(),
                    padding=ft.padding.all(25),
                    bgcolor="#a9a1f9",
                    color=ft.Colors.WHITE
                ),
            ),
            right=20,
            bottom=20,
        )

        stack_layout = ft.Stack(
            [
                main_content,
                floating_button_container
            ],
            expand=True
        )

        return ft.View(
            route="/home",
            controls=[
                ft.AppBar(
                    title=ft.Text("Minhas Senhas"),
                    bgcolor="#544E9E",
                ),
                stack_layout
            ],
            drawer=drawer,
        )

    def create_config_view():
        page.title = "Felichia - Minhas Notas"

        drawer = build_app_drawer(page)

        return ft.View(
            route="/config",
            controls=[
                ft.AppBar(
                    title=ft.Text("Configurações"),
                    bgcolor="#544E9E",
                ),
                ft.Column(
                    [
                        ft.Text("Configurações", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Seu conteúdo e listas virão aqui..."),
                        ft.Container(height=300),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    expand=True
                )
            ],
            drawer=drawer,
        )

    def route_change(route):
        page.views.clear()

        if page.route == "/":
            page.views.append(create_login_view())

        elif page.route == "/register":
            page.views.append(create_register_view())

        elif page.route == "/home":
            page.views.append(create_home_view())

        elif page.route == "/notas":
            page.views.append(create_notas_view())

        elif page.route == "/config":
            page.views.append(create_config_view())

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)


if __name__ == "__main__":
    ft.app(main)
