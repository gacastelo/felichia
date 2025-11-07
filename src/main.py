import flet as ft
import sys
import os

from flet.core.textfield import NumbersOnlyInputFilter
from rich.jupyter import display

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from core.database import Database
from controllers.authController import AuthController
from controllers.credencialController import CredencialController

from utils.utils import check_password_strength, gerar_senha_randomica, decrypt_password


def setup():
    db = Database()
    db.setup()


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
        if page.session.get("user_id") is None:
            page.go("/")
        credencial_controller = CredencialController()

        user_id = page.session.get("user_id")
        chave = page.session.get("chave")
        
        credenciais_ui_list = []

        all_credenciais = credencial_controller.listar_credenciais(user_id, chave)
        for credencial in all_credenciais:
            credenciais_ui_list.append(
                ft.Container(
                    content=
                    ft.Column([
                        ft.Row([
                            ft.Container(expand=True),
                            ft.Text(f"Titulo: {credencial[0]}"),  # Ex: Titulo
                            ft.Container(expand=True),
                            ft.Text(f"Site: {credencial[1]}"),  # Ex: Login
                            ft.Container(expand=True),
                            ft.Text(f"Login: {credencial[2]}"),  # Ex: Site
                            ft.Container(expand=True),
                            #ft.Text(f"Senha: {decrypt_password(chave, credencial[3], credencial[4])}")  # Ex: Senha Cifrada
                        ]),
                        ft.Row([
                            ft.TextButton("Copiar Senha", expand=1, adaptive=True),
                            ft.TextButton("Copiar Login", expand=1, adaptive=True),
                            ft.TextButton("Editar", expand=1, adaptive=True),
                            ft.TextButton("Excluir", expand=1, adaptive=True)
                        ],
                            run_spacing=0,
                            spacing=0,
                            expand=True,
                            #visible=False
                        )
                    ]),
                    border=ft.border.all(1, "#544E9E"),
                    border_radius=5,

                )
            )

        list_content = ft.Column(
        controls=credenciais_ui_list,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )

        page.title = "Felichia - Minhas Senhas"

        drawer = build_app_drawer(page)


        def save_credential(e):
            credencial_controller.salvar_credencial(user_id, chave, titulo_field.value, login_field.value, site_field.value, senha_field.value)
            close_dlg(e)

        # Modal Nova Senha

        def close_dlg(e):
            dlg_modal.open = False
            e.control.page.update()

        titulo_field = ft.TextField(label="Titulo", width=300, icon=ft.Icons.TITLE)
        login_field = ft.TextField(label="Login", width=300, icon=ft.Icons.PERSON_OUTLINE)
        site_field = ft.TextField(label="Site", width=300, icon=ft.Icons.WEB)
        senha_field = ft.TextField(label="Senha", width=300, icon=ft.Icons.LOCK_OUTLINE, password=True,
                                   can_reveal_password=True)
        confirma_senha_field = ft.TextField(label="Confirme sua Senha", width=300, password=True,
                                            can_reveal_password=True, icon=ft.Icons.LOCK_OUTLINE)

        strength_indicator_text = ft.Text("Força da Senha: ", size=12, visible=False)
        password_strength_bar = ft.Container(
            height=8,
            width=0,
            bgcolor=ft.Colors.TRANSPARENT,
            border_radius=5,
            animate_size=300
        )

        randomizer_text = ft.Text("", size=10, visible=False, color=ft.Colors.RED_900)

        save_button = ft.TextButton("Salvar", on_click=save_credential, disabled=True)

        special_caracter_checkbox = ft.Checkbox(
            value=True,
            label="Caracteres especiais"
        )

        def validate_fields(e):
            all_fields_filled = bool(
                titulo_field.value and login_field.value and site_field.value and senha_field.value and confirma_senha_field.value)

            passwords_match = senha_field.value == confirma_senha_field.value

            strength_result = check_password_strength(senha_field.value)
            if senha_field.value:
                strength_indicator_text.visible = True
            else:
                strength_indicator_text.visible = False
            strength_indicator_text.value = f"Força da Senha: {strength_result['strength']}"

            password_strength_bar.width = 300 * strength_result['width_factor']
            password_strength_bar.bgcolor = strength_result['color']

            is_valid = all_fields_filled and passwords_match and strength_result['score'] >= 2

            if save_button.disabled == is_valid:
                save_button.disabled = not is_valid
                e.control.page.update()

            dlg_modal.update()

        def verify_size_randomizer(e):
            if not e.control.value:
                randomizer_text.visible = False
                randomizer_button.disabled = True
                randomizer_button.style = ft.ButtonStyle(bgcolor="#363285", color=ft.Colors.GREY)
            elif int(e.control.value) < 8:
                randomizer_text.value = "*Tamanho mínimo de 8 caracteres"
                randomizer_text.visible = True
                randomizer_button.disabled = True
                randomizer_button.style = ft.ButtonStyle(bgcolor="#363285", color=ft.Colors.GREY)
            elif int(e.control.value) > 64:
                randomizer_text.value = "*Tamanho máximo de 64 caracteres"
                randomizer_text.visible = True
                randomizer_button.disabled = True
                randomizer_button.style = ft.ButtonStyle(bgcolor="#363285", color=ft.Colors.GREY)
            else:
                randomizer_text.visible = False
                randomizer_button.disabled = False
                randomizer_button.style = ft.ButtonStyle(bgcolor="#544E9E", color=ft.Colors.WHITE)
            e.control.page.update()
            randomizer_text.update()


        randomizer_field = ft.TextField(
            label="Tamanho da Senha",
            hint_text="8",
            value="8",
            width=150,
            icon=ft.Icons.PASSWORD,
            on_change=verify_size_randomizer,
            input_filter=NumbersOnlyInputFilter(),
            max_length=2,
            text_align=ft.TextAlign.CENTER,

        )

        def gerar_senha(e):
            senha_field.value = confirma_senha_field.value = gerar_senha_randomica(int(randomizer_field.value), special_caracter_checkbox.value)
            validate_fields(e)
            page.update()

        randomizer_button = ft.ElevatedButton(
            text="Gerar Senha",
            on_click=gerar_senha,
            width=125, style=ft.ButtonStyle(bgcolor="#544E9E", color=ft.Colors.WHITE)
        )

        titulo_field.on_change = validate_fields
        login_field.on_change = validate_fields
        site_field.on_change = validate_fields
        senha_field.on_change = validate_fields
        confirma_senha_field.on_change = validate_fields

        dlg_modal = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                expand=True,

                content=ft.Column([

                    ft.Row(
                        [
                            ft.Text("Adicionar Senha", size=20, weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER)
                        ], width=300, alignment=ft.MainAxisAlignment.CENTER
                    ),

                    # Campos de entrada
                    titulo_field,
                    login_field,
                    site_field,
                    senha_field,
                    confirma_senha_field,

                    # Indicador de Força
                    ft.Container(
                        content=ft.Column(
                            [
                                strength_indicator_text,
                                ft.Row([
                                    password_strength_bar,
                                    ft.Container(expand=True)
                                ], spacing=0)
                            ],
                            spacing=5
                        ),
                        width=300,
                        padding=ft.padding.only(left=0, right=0, bottom=5)
                    ),

                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row([
                                    ft.Text("Gerador de Senhas", size=20, weight=ft.FontWeight.BOLD,
                                            text_align=ft.TextAlign.CENTER)
                                ], width=300, alignment=ft.MainAxisAlignment.CENTER),

                                ft.Row([
                                    randomizer_field,
                                    randomizer_button,
                                ], width=300, alignment=ft.MainAxisAlignment.CENTER),

                                randomizer_text,
                                ft.Row(
                                    [
                                        special_caracter_checkbox
                                    ],
                                    width=300, alignment=ft.MainAxisAlignment.CENTER
                                )
                            ]
                        ),
                        padding=ft.padding.only(top=15, bottom=0)
                    ),

                    ft.Container(height=20)

                ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dlg),
                save_button,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        def button_click(e):
            e.control.page.overlay.append(dlg_modal)
            dlg_modal.open = True
            e.control.page.update()

        # Main Content

        main_content = ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Home", size=24, weight=ft.FontWeight.BOLD),
                        ],
                        expand=4,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row([
                        list_content if all_credenciais else ft.Text("Nenhuma credencial cadastrada. Clique em '+' para adicionar uma."),
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
            on_click=button_click,
            bgcolor="#a9a1f9",
        )

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
