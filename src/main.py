import flet as ft
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from controllers.authController import AuthController
from controllers.credencialController import CredencialController
from controllers.noteController import NoteController

from utils.utils import setup, decrypt, toggle_theme
from utils.buildAppDrawer import build_app_drawer
from utils.credencialCard import CredencialCard
from utils.noteCard import NoteCard
from utils.addCredencialModal import AddCredencialModal
from utils.editCredencialModal import EditCredencialModal
from core.config import load_settings

global logged

def is_logged(page: ft.Page):
    global logged
    if page.session.get("user_id") is None or page.session.get("chave") is None or not logged:
        page.clean()
        page.go("/")
        page.update()

def logout(page: ft.Page):
    global logged
    logged = False
    page.session.set("user_id", None)
    page.session.set("chave", None)
    page.go("/")
    page.update()

def main(page: ft.Page):
    global logged
    logged = False
    auth_controller = AuthController()

    settings = load_settings()

    page.title = "Felichia"
    page.theme_mode = ft.ThemeMode.LIGHT if settings["theme"] == "light" else ft.ThemeMode.DARK

    def create_login_view():
        page.title = "Felichia - Login"

        username_field = ft.TextField(label="Username", width=300, icon=ft.Icons.PERSON_OUTLINE)
        senha_field = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300,
                                   icon=ft.Icons.LOCK_OUTLINE)

        def handle_login(e):
            global logged
            if username_field.value and senha_field.value:
                status, user_id, chave = auth_controller.login(username_field.value, senha_field.value)
                if status == "Senha incorreta." or status == "Usuário não encontrado.":
                    page.open(ft.SnackBar(ft.Text(status, weight=ft.FontWeight.BOLD), bgcolor="#a9a1f9"))
                page.update()
                if user_id and chave:
                    page.session.set("user_id", user_id)
                    page.session.set("chave", chave)
                    logged = True
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

        all_credenciais_cache = credencial_controller.listar_credenciais(user_id)

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

        drawer = build_app_drawer(page, logout)


        # Modal Nova Senha
        def on_new_credential_saved():
            all_credenciais_cache[:] = credencial_controller.listar_credenciais(user_id)
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
                    ft.Container(height=10),
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
            #border=ft.border.all(1, "#544E9E"),
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
                    title=ft.Text("Minhas Senhas", color="#FFFFFF"),
                    bgcolor="#544E9E",
                ),
                main_content,
            ],
            drawer=drawer,
            floating_action_button=fab_add
        )

    def create_notas_view():
        is_logged(page)
        user_id = page.session.get("user_id")
        chave = page.session.get("chave")

        note_controller = NoteController()

        page.title = "Felichia - Minhas Notas"

        drawer = build_app_drawer(page, logout)

        def open_note_editor(note_id: int):
            page.go(f"/nota/edit/{note_id}")

        def button_click(e):
            new_note = note_controller.criar_nota(user_id)
            open_note_editor(new_note)
            page.update()

        all_notes_cache = note_controller.listar_notas(user_id)

        list_content = ft.Column(
            controls=[],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        search_bar = ft.SearchBar(
            bar_hint_text="Buscar minhas notas...",
            width = (page.width * 0.75),
            on_change=lambda e: refresh_notas_list()
        )


        def refresh_notas_list():

            def handle_card_deleted(card_to_remove: NoteCard):
                note_id_to_remove = card_to_remove.note_data[0]
                all_notes_cache[:] = [c for c in all_notes_cache if c[0] != note_id_to_remove]

                refresh_notas_list()

            search_term = search_bar.value.lower()

            list_content.controls.clear()

            filtered_list = []
            if search_term:
                for nota in all_notes_cache:
                    titulo = str(nota[1]).lower()

                    if search_term in titulo:
                        filtered_list.append(nota)
            else:
                filtered_list = all_notes_cache

            if filtered_list:
                for nota in filtered_list:
                    nota_id_atual = nota[0]
                    card = NoteCard(
                        note_data=nota,
                        user_id=user_id,
                        chave=chave,
                        controller=note_controller,
                        on_delete=handle_card_deleted,
                        open_editor_func=lambda _, id_do_card=nota_id_atual: open_note_editor(id_do_card)
                    )
                    list_content.controls.append(card)

            elif not all_notes_cache:
                list_content.controls.append(
                    ft.Text("Nenhuma nota cadastrada. Clique em '+' para adicionar uma.")
                )
            else:
                list_content.controls.append(
                    ft.Text(f"Nenhum resultado encontrado para '{search_bar.value}'")
                )

            if list_content.page:
                list_content.update()

        main_content = ft.Container(
            ft.Column(
                [
                    ft.Container(height=10),
                    ft.Row(
                        [
                            ft.Text("Minhas Notas", size=30, weight=ft.FontWeight.BOLD),
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
                        wrap=True,
                    ),
                    ft.Container(height=300),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,

            ),
            #border=ft.border.all(1, "#544E9E"),
            expand=4
        )

        fab_add = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            on_click=button_click,
            bgcolor="#a9a1f9"
        )

        refresh_notas_list()

        return ft.View(
            route="/notas",
            controls=[
                ft.AppBar(
                    title=ft.Text("Minhas Notas", color="#FFFFFF"),
                    bgcolor="#544E9E",
                ),
                main_content
            ],
            drawer=drawer,
            floating_action_button=fab_add
        )

    def create_note_editor_view(page: ft.Page, note_id: int):
        is_logged(page)
        user_id = page.session.get("user_id")
        chave = page.session.get("chave")

        note_controller = NoteController()
        note_data = note_controller.buscar_nota_por_id(user_id, note_id)

        # 2. Campos de Edição
        title_field = ft.TextField(
            value=note_data[1],
            label="Título da Nota",
            width=400,
            border_color="#A9A1F9"
        )

        content_field = ft.TextField(
            value=decrypt(chave, note_data[2], note_data[3]) if (note_data[2] and note_data[3]) else "",
            hint_text="Comece a escrever sua nota aqui...",
            multiline=True,
            min_lines=20,
            expand=True,
            border_color="#544E9E"
        )

        def save_note(e):
            note_controller.editar_nota(
                user_id,
                chave,
                note_id,
                title_field.value,
                content_field.value
            )
            page.go("/notas")
            page.open(ft.SnackBar(ft.Text("Nota Salva!"), bgcolor="#a9a1f9"))
            page.update()

        def delete_note(e):
            note_controller.excluir_nota(user_id, note_id)
            page.go("/notas")
            page.open(ft.SnackBar(ft.Text("Nota Excluida!"), bgcolor="#a9a1f9"))
            page.update()

        return ft.View(
            route=f"/nota/edit/{note_id}",
            controls=[
                ft.AppBar(
                    title=ft.Text("Editar Nota", color="#FFFFFF"),
                    bgcolor="#544E9E",
                    leading=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda e: page.go("/notas")
                    ),
                    actions=[
                        ft.ElevatedButton("Salvar", on_click=save_note, icon=ft.Icons.SAVE, color="#a9a1f9"),
                        ft.Container(width=10),
                        ft.ElevatedButton("Excluir",on_click=delete_note, icon=ft.Icons.DELETE, color="#a9a1f9"),
                        ft.Container(width=10)
                    ]
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            title_field,
                            content_field,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        scroll=ft.ScrollMode.ADAPTIVE,
                        expand=True
                    ),
                    padding=20,
                    expand=True
                )
            ]
        )

    def create_config_view():
        is_logged(page)
        #Todo importar/exportar dados, Troca de Tema(adaptar outras paginas a isso), e possível sincronização entre dispositivos
        page.title = "Felichia - Configurações"

        drawer = build_app_drawer(page, logout)

        main_content = ft.Container(
                ft.Column(
                [
                    ft.Container(height=10),
                    ft.Text("Configurações", size=30, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        ft.Column(
                            [
                                ft.Text("Tema", weight=ft.FontWeight.BOLD, size=20),
                                ft.Switch(label="Light Theme", value=(page.theme_mode == ft.ThemeMode.LIGHT), on_change= toggle_theme)
                            ]
                        ),
                        width=(page.width * 0.9),
                        padding=50,
                    ),
                    ft.Container(height=300),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            )
        )

        return ft.View(
            route="/config",
            controls=[
                ft.AppBar(
                    title=ft.Text("Configurações", color="#FFFFFF"),
                    bgcolor="#544E9E",
                ),
                main_content
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
            is_logged(page)
            page.views.append(create_home_view())

        elif page.route == "/notas":
            is_logged(page)
            page.views.append(create_notas_view())

        elif page.route.startswith("/nota/edit/"):
            is_logged(page)
            note_id = int(page.route.split("/")[-1])
            page.views.append(create_note_editor_view(page, note_id))

        elif page.route == "/config":
            is_logged(page)
            page.views.append(create_config_view())

        elif page.route == "/logout":
            logout(page)

        page.update()

    page.on_route_change = route_change

    page.go(page.route)


if __name__ == "__main__":
    setup()
    ft.app(main)
