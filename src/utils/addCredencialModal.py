import flet as ft
from utils.utils import check_password_strength, gerar_senha_randomica, decrypt_password

class AddCredencialModal(ft.AlertDialog):
    def __init__(self, user_id, chave, credencialController,on_save_success):
        super().__init__()

        self.user_id = user_id
        self.chave = chave
        self.credencial_controller = credencialController
        self.on_save_callback = on_save_success

        self.titulo_field = ft.TextField(label="Titulo", width=300, icon=ft.Icons.TITLE)
        self.login_field = ft.TextField(label="Login", width=300, icon=ft.Icons.PERSON_OUTLINE)
        self.site_field = ft.TextField(label="Site", width=300, icon=ft.Icons.LANGUAGE_OUTLINED)
        self.senha_field = ft.TextField(label="Senha", width=300, icon=ft.Icons.LOCK_OUTLINE, password=True,can_reveal_password=True)
        self.confirma_senha_field = ft.TextField(label="Confirme sua Senha", width=300, password=True, can_reveal_password=True, icon=ft.Icons.LOCK_OUTLINE)

        self.titulo_field.on_change = lambda _: self.validate_fields()
        self.login_field.on_change = lambda _: self.validate_fields()
        self.site_field.on_change = lambda _: self.validate_fields()
        self.senha_field.on_change = lambda _: self.validate_fields()
        self.confirma_senha_field.on_change = lambda _: self.validate_fields()

        self.strength_indicator_text = ft.Text("Força da Senha: ", size=12, visible=False)
        self.password_strength_bar = ft.Container(
            height=8,
            width=0,
            bgcolor=ft.Colors.TRANSPARENT,
            border_radius=5,
            animate_size=300
        )

        self.randomizer_field = ft.TextField(
            label="Tamanho da Senha",
            hint_text="8",
            value="8",
            width=150,
            icon=ft.Icons.PASSWORD,
            on_change=self.verify_size_randomizer,
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=2,
            text_align=ft.TextAlign.CENTER,

        )

        self.randomizer_text = ft.Text("", size=10, visible=False, color=ft.Colors.RED_900)

        self.save_button = ft.TextButton("Salvar", on_click= self.save_credential, disabled=True)

        self.special_caracter_checkbox = ft.Checkbox(
            value=True,
            label="Caracteres especiais"
        )

        self.randomizer_button = ft.ElevatedButton(
            text="Gerar Senha",
            on_click=lambda _: self.gerar_senha(),
            width=125, style=ft.ButtonStyle(bgcolor="#544E9E", color=ft.Colors.WHITE)
        )

        self.actions = [
            ft.TextButton("Cancelar", on_click= self.close_dlg),
            self.save_button,
        ]

        self.content = ft.Container(
            expand=True,
            content=ft.Column([

                    ft.Row(
                        [
                            ft.Text("Adicionar Senha", size=20, weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER)
                        ], width=300, alignment=ft.MainAxisAlignment.CENTER
                    ),

                    # Campos de entrada
                    self.titulo_field,
                    self.login_field,
                    self.site_field,
                    self.senha_field,
                    self.confirma_senha_field,

                    # Indicador de Força
                    ft.Container(
                        content=ft.Column(
                            [
                                self.strength_indicator_text,
                                ft.Row([
                                    self.password_strength_bar,
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
                                    self.randomizer_field,
                                    self.randomizer_button,
                                ], width=300, alignment=ft.MainAxisAlignment.CENTER),

                                self.randomizer_text,
                                ft.Row(
                                    [
                                        self.special_caracter_checkbox
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
        )

    def validate_fields(self):
        all_fields_filled = bool(
            self.titulo_field.value and self.login_field.value and self.site_field.value and self.senha_field.value and self.confirma_senha_field.value)

        passwords_match = self.senha_field.value == self.confirma_senha_field.value

        strength_result = check_password_strength(self.senha_field.value)
        if self.senha_field.value:
            self.strength_indicator_text.visible = True
        else:
            self.strength_indicator_text.visible = False
        self.strength_indicator_text.value = f"Força da Senha: {strength_result['strength']}"

        self.password_strength_bar.width = 300 * strength_result['width_factor']
        self.password_strength_bar.bgcolor = strength_result['color']

        is_valid = all_fields_filled and passwords_match and strength_result['score'] >= 2

        if self.save_button.disabled == is_valid:
            self.save_button.disabled = not is_valid

        self.update()


    def verify_size_randomizer(self, e):
        if not e.control.value:
            self.randomizer_text.visible = False
            self.randomizer_button.disabled = True
            self.randomizer_button.style = ft.ButtonStyle(bgcolor="#363285", color=ft.Colors.GREY)
        elif int(e.control.value) < 8:
            self.randomizer_text.value = "*Tamanho mínimo de 8 caracteres"
            self.randomizer_text.visible = True
            self.randomizer_button.disabled = True
            self.randomizer_button.style = ft.ButtonStyle(bgcolor="#363285", color=ft.Colors.GREY)
        elif int(e.control.value) > 64:
            self.randomizer_text.value = "*Tamanho máximo de 64 caracteres"
            self.randomizer_text.visible = True
            self.randomizer_button.disabled = True
            self.randomizer_button.style = ft.ButtonStyle(bgcolor="#363285", color=ft.Colors.GREY)
        else:
            self.randomizer_text.visible = False
            self.randomizer_button.disabled = False
            self.randomizer_button.style = ft.ButtonStyle(bgcolor="#544E9E", color=ft.Colors.WHITE)
        e.control.page.update()
        self.randomizer_text.update()

    def gerar_senha(self):
        self.senha_field.value = self.confirma_senha_field.value = gerar_senha_randomica(int(self.randomizer_field.value), self.special_caracter_checkbox.value)
        self.validate_fields()

    def save_credential(self, e):
        try:
            self.credencial_controller.salvar_credencial(
                self.user_id,
                self.chave,
                self.titulo_field.value,
                self.login_field.value,
                self.site_field.value,
                self.senha_field.value
            )

            if self.on_save_callback:
                self.on_save_callback()

            self.close_dlg(e)

        except Exception as ex:
            print(f"Erro ao salvar: {ex}")

    def close_dlg(self, e):
        self.open = False
        self.clear()
        if self.page:
            self.page.update()

    def clear(self):
        self.titulo_field.value = ""
        self.login_field.value = ""
        self.site_field.value = ""
        self.senha_field.value = ""
        self.confirma_senha_field.value = ""
        self.randomizer_field.value = "8"
        self.special_caracter_checkbox.value = True
        self.strength_indicator_text.visible = False
        self.password_strength_bar.width = 0
        self.password_strength_bar.bgcolor = ft.Colors.TRANSPARENT
        self.randomizer_text.visible = False