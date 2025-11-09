import flet as ft
from utils.utils import check_password_strength, gerar_senha_randomica, decrypt_password

class CredencialCard(ft.Container):

    def __init__(self, credencial_data: tuple, user_id: int, chave: str, controller, on_delete, open_edit_modal_func):
        super().__init__()

        self.credencial_data = credencial_data
        self.user_id = user_id
        self.chave = chave
        self.controller = controller
        self.on_delete_callback = on_delete
        self.open_edit_modal_func = open_edit_modal_func

        cred_id = self.credencial_data[0]
        cred_titulo = self.credencial_data[1]
        cred_site = self.credencial_data[2]
        cred_login = self.credencial_data[3]
        cred_senha = self.credencial_data[4]
        cred_nonce = self.credencial_data[5]

        # 2. Define os controles internos
        self.buttons_row = ft.Row(
            [
                ft.TextButton("Copiar Senha", expand=1, adaptive=True, key=cred_id,
                              data={"action": "copiar_senha", "senha": cred_senha, "nonce": cred_nonce},
                              on_click=self.handle_button_action),
                ft.TextButton("Copiar Login", expand=1, adaptive=True, key=cred_id,
                              data={"action": "copiar_login", "login": cred_login},
                              on_click=self.handle_button_action),
                ft.TextButton("Editar", expand=1, adaptive=True, key=cred_id,
                              data={"action": "editar", "credencial_id": cred_id, "titulo": cred_titulo, "site": cred_site, "login": cred_login, "senha": cred_senha, "nonce": cred_nonce},
                              on_click=self.handle_button_action),
                ft.TextButton("Excluir", expand=1, adaptive=True, key=cred_id,
                              data={"action": "excluir", "id": cred_id},
                              on_click=self.handle_button_action)
            ],
            run_spacing=0, spacing=0, expand=True, visible=False,
            key=f"buttons_{cred_id}"
        )

        self.info_row = ft.Row(
            [
                ft.Icon(ft.Icons.TITLE, color="#363285", size=20),
                ft.Text(f"{cred_titulo}", size=16, weight=ft.FontWeight.W_500, color="#E0E0E0"),
                ft.VerticalDivider(width=1),
                ft.Icon(ft.Icons.LANGUAGE_OUTLINED, color="#491C6E", size=20),
                ft.Text(f"{cred_site}", size=14, italic=True, color="#E0E0E0"),
                ft.VerticalDivider(width=1),
                ft.Icon(ft.Icons.PERSON_OUTLINE, color="#A9A1F9", size=20),
                ft.Text(f"{cred_login}", size=14, color="#E0E0E0"),
            ],
            alignment=ft.MainAxisAlignment.START,
        )

        self.content = ft.Column([self.info_row, self.buttons_row])
        self.border = ft.border.all(1, "#544E9E")
        self.border_radius = 5
        self.padding = 10
        self.on_tap_down = self.handle_tap
        self.on_hover = self.handle_hover

    # ---- Métodos de Ação ----

    def handle_tap(self, e):
        self.buttons_row.visible = not self.buttons_row.visible
        self.update()

    def handle_hover(self, e):
        self.bgcolor = "#0D1117" if e.data == "true" else None
        self.update()

    def handle_button_action(self, e):
        action = e.control.data['action']

        if not self.page:
            return

        if action == "copiar_senha":
            decrypted = decrypt_password(self.chave, e.control.data['senha'], e.control.data['nonce'])
            self.page.set_clipboard(decrypted)
            self.page.open(ft.SnackBar(ft.Text("Senha Copiada para a Área de Transferência", weight=ft.FontWeight.BOLD),
                                       bgcolor="#a9a1f9"))

        elif action == "copiar_login":
            self.page.set_clipboard(e.control.data['login'])
            self.page.open(ft.SnackBar(ft.Text("Login Copiado para a Área de Transferência", weight=ft.FontWeight.BOLD),
                                       bgcolor="#a9a1f9"))


        elif action == "editar":
            credencial_id = e.control.data['credencial_id']

            initial_data = {
                'titulo': e.control.data['titulo'],
                'site': e.control.data['site'],
                'login': e.control.data['login'],
                'senha': decrypt_password(self.chave, e.control.data['senha'], e.control.data['nonce']),
                'nonce': e.control.data['nonce']

            }

            self.open_edit_modal_func(credencial_id, initial_data)

        elif action == "excluir":
            credential_id_to_delete = e.control.data['id']

            confirm_dialog = ft.AlertDialog(
                title=ft.Text("Excluir Credencial"),
                content=ft.Text("Tem certeza que deseja excluir esta credencial?"),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda _: self.page.close(confirm_dialog)),
                    ft.TextButton("Excluir",
                                  on_click=lambda _: self.do_delete_credential(confirm_dialog, credential_id_to_delete))
                ]
            )
            self.page.open(confirm_dialog)

    def do_delete_credential(self, dialog, credential_id):
        """Ação final de exclusão, chamada pelo diálogo."""
        try:
            self.controller.excluir_credencial(self.user_id, credential_id)

            self.page.close(dialog)

            if self.on_delete_callback:
                self.on_delete_callback(self)

        except Exception as ex:
            print(f"Erro ao excluir credencial: {ex}")
            self.page.open(ft.SnackBar(ft.Text(f"Erro ao excluir: {ex}"), bgcolor=ft.Colors.RED))
