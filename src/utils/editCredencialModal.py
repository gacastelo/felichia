import flet as ft
from utils.utils import check_password_strength, gerar_senha_randomica, decrypt_password
from utils.addCredencialModal import AddCredencialModal

class EditCredencialModal(AddCredencialModal):
    def __init__(self, user_id, chave, credencialController,on_save_success, credencial_id:int):
        super().__init__(user_id, chave, credencialController,on_save_success)


        self.save_button = ft.TextButton("Editar", on_click=self.edit_credencial, disabled=True)

        self.credencial_id = credencial_id

        self.actions = [
            ft.TextButton("Cancelar", on_click=self.close_dlg),
            self.save_button,
        ]

        self.content = ft.Container(
            expand=True,
            content=ft.Column([

                ft.Row(
                    [
                        ft.Text("Editar Senha", size=20, weight=ft.FontWeight.BOLD,
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

    def edit_credencial(self, e):
        try:
            self.credencial_controller.editar_credencial(
                self.user_id,
                self.chave,
                self.credencial_id,
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