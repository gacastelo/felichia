import flet as ft

class NoteCard(ft.Container):
    def __init__(self, note_data: tuple, user_id: int, chave: str, controller, on_delete, open_editor_func):
        super().__init__()
        self.note_data = note_data
        self.user_id = user_id
        self.chave = chave
        self.controller = controller
        self.on_delete = on_delete
        self.open_editor_func = open_editor_func

        self.note_id = note_data[0]
        self.note_title = note_data[1]
        self.note_content = note_data[2]
        self.note_nonce = note_data[3]


        self.info_row = ft.Row(
            [
                ft.Icon(ft.Icons.TITLE, color="#363285", size=20),
                ft.Text(f"{self.note_title}", size=16, weight=ft.FontWeight.W_500),
            ],
            alignment=ft.MainAxisAlignment.START,
        )

        self.content = ft.Column([self.info_row])
        self.border = ft.border.all(1, "#544E9E")
        self.border_radius = 5
        self.padding = 10
        self.on_tap_down = self.handle_tap
        self.on_hover = self.handle_hover

    def handle_tap(self, e):
        self.open_editor_func(self.note_id)
        self.page.update()

    def handle_hover(self, e):
        self.bgcolor = ("#0D1117" if self.page.theme_mode == ft.ThemeMode.DARK else "#E0E0E0") if e.data == "true" else None
        self.update()
