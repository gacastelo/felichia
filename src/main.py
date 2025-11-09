import flet as ft
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from controllers.authController import AuthController
from controllers.credencialController import CredencialController

from utils.utils import setup

from utils.buildAppDrawer import build_app_drawer
from utils.credencialCard import CredencialCard
from utils.addCredencialModal import AddCredencialModal
from utils.editCredencialModal import EditCredencialModal



def is_logged(page: ft.Page):
    if page.session.get("user_id") is None:
        page.go("/")

def main(page: ft.Page):
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
                    page.session.set("user_id", user_id)
                    page.session.set("chave", chave)
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
        is_logged(page)
        credencial_controller = CredencialController()
        user_id = page.session.get("user_id")
        chave = page.session.get("chave")

        all_credenciais_cache = credencial_controller.listar_credenciais(user_id, chave)

        list_content = ft.Column(
            controls=[],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        search_bar = ft.SearchBar(
                        bar_hint_text="Buscar minhas senhas...",
                        width = (page.width * 0.75),
                        on_change=lambda e: refresh_credenciais_list()
                      )

        def refresh_credenciais_list():

            def handle_card_deleted(card_to_remove: CredencialCard):
                cred_id_to_remove = card_to_remove.credencial_data[0]
                all_credenciais_cache[:] = [c for c in all_credenciais_cache if c[0] != cred_id_to_remove]

                refresh_credenciais_list()

            search_term = search_bar.value.lower()

            list_content.controls.clear()

            filtered_list = []
            if search_term:
                for cred in all_credenciais_cache:
                    titulo = str(cred[1]).lower()
                    site = str(cred[2]).lower()
                    login = str(cred[3]).lower()

                    if search_term in titulo or search_term in site or search_term in login:
                        filtered_list.append(cred)
            else:
                filtered_list = all_credenciais_cache

            if filtered_list:
                for credencial in filtered_list:
                    card = CredencialCard(
                        credencial_data=credencial,
                        user_id=user_id,
                        chave=chave,
                        controller=credencial_controller,
                        on_delete=handle_card_deleted,
                        open_edit_modal_func=open_edit_modal
                    )
                    list_content.controls.append(card)
            elif not all_credenciais_cache:
                list_content.controls.append(
                    ft.Text("Nenhuma credencial cadastrada. Clique em '+' para adicionar uma.")
                )
            else:
                list_content.controls.append(
                    ft.Text(f"Nenhum resultado encontrado para '{search_bar.value}'")
                )

            if list_content.page:
                list_content.update()

        page.title = "Felichia - Minhas Senhas"
        drawer = build_app_drawer(page)


        # Modal Nova Senha
        def on_new_credential_saved():
            all_credenciais_cache[:] = credencial_controller.listar_credenciais(user_id, chave)
            refresh_credenciais_list()

        add_credencial_dialog = AddCredencialModal(
            user_id=user_id,
            chave=chave,
            credencialController=credencial_controller,
            on_save_success=on_new_credential_saved
        )

        def open_add_modal(e):
            page.overlay.append(add_credencial_dialog)
            add_credencial_dialog.open = True
            page.update()

        def open_edit_modal(credencial_id: int, initial_data: dict):
            edit_dialog = EditCredencialModal(
                user_id=user_id,
                chave=chave,
                credencialController=credencial_controller,
                on_save_success=on_new_credential_saved,
                credencial_id=credencial_id
            )

            edit_dialog.titulo_field.value = initial_data['titulo']
            edit_dialog.site_field.value = initial_data['site']
            edit_dialog.login_field.value = initial_data['login']
            edit_dialog.senha_field.value = initial_data['senha']


            page.overlay.append(edit_dialog)
            edit_dialog.open = True
            page.update()

        main_content = ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Minhas Senhas", size=30, weight=ft.FontWeight.BOLD),
                        ],
                        expand=4,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [
                            search_bar
                        ],
                        expand=4,
                        alignment=ft.MainAxisAlignment.CENTER,
                        adaptive=True
                    ),
                    ft.Row([
                        list_content,
                    ],
                    expand=4,
                    alignment=ft.MainAxisAlignment.CENTER,
                    width=(page.width * 0.8),
                    wrap = True,
                    ),
                    ft.Container(height=300),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,

            ),
            border=ft.border.all(1, "#544E9E"),
            expand=4
        )

        fab_add = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            on_click=open_add_modal,
            bgcolor="#a9a1f9",
        )

        refresh_credenciais_list()

        return ft.View(
            route="/home",
            controls=[
                ft.AppBar(
                    title=ft.Text("Minhas Senhas"),
                    bgcolor="#544E9E",
                ),
                main_content,
            ],
            drawer=drawer,
            floating_action_button=fab_add
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

        fab_add = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            on_click=button_click,
            bgcolor="#a9a1f9"
        )

        return ft.View(
            route="/notas",
            controls=[
                ft.AppBar(
                    title=ft.Text("Minhas Notas"),
                    bgcolor="#544E9E",
                ),
                main_content
            ],
            drawer=drawer,
            floating_action_button=fab_add
        )

    def create_config_view():
        page.title = "Felichia - Configurações"

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

    page.on_route_change = route_change

    page.go(page.route)


if __name__ == "__main__":
    setup()
    ft.app(main)
