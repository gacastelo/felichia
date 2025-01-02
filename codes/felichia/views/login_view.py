from views.base_view import BaseView
import customtkinter as ctk
from views.popups.base_popup import BasePopup
from views.popups.mensagem_popup import MensagemPopup

class LoginView(BaseView):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Felichia - Login")
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Frame central
        frame_central = ctk.CTkFrame(self)
        frame_central.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        titulo = ctk.CTkLabel(
            frame_central,
            text="LOGIN",
            font=("Roboto", 24, "bold")
        )
        titulo.pack(pady=20)
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(
            frame_central,
            text="Informe seu nome de usuário e senha para continuar",
            font=("Roboto", 12)
        )
        subtitulo.pack(pady=10)
        
        # Campo de usuário
        self.username_entry = ctk.CTkEntry(
            frame_central,
            placeholder_text="Nome de usuário",
            width=300
        )
        self.username_entry.pack(pady=10)
        
        # Campo de senha
        self.password_entry = ctk.CTkEntry(
            frame_central,
            placeholder_text="Senha",
            show="•",
            width=300
        )
        self.password_entry.pack(pady=10)
        
        # Frame para botões
        frame_botoes = ctk.CTkFrame(frame_central, fg_color="transparent")
        frame_botoes.pack(pady=20)
        
        # Botão de login
        btn_login = ctk.CTkButton(
            frame_botoes,
            text="Entrar",
            command=self._fazer_login,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_login.pack(side="left", padx=5)
        
        # Botão de cadastro
        btn_cadastro = ctk.CTkButton(
            frame_botoes,
            text="Cadastrar",
            command=self._abrir_cadastro,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_cadastro.pack(side="left", padx=5)
        
        # Botão de sair
        btn_sair = ctk.CTkButton(
            frame_botoes,
            text="Sair",
            command=self.master.destroy,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_sair.pack(side="left", padx=5)
        
        # Bind Enter para login
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self._fazer_login())
    
    def _fazer_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
    
        if not username or not password:
            self._mostrar_erro("Preencha todos os campos!")
            return
    
        # Chama o método de login do controlador de autenticação
        sucesso, mensagem = self.master.auth_controller.login(username, password)
    
        if sucesso:
            self._abrir_gerenciador()
        else:
            # Exibe mensagem de erro caso o login falhe
            self._mostrar_erro(mensagem)
            # Limpa o campo de senha
            self.password_entry.delete(0, "end")

    
    def _abrir_cadastro(self):
        from views.cadastro_view import CadastroView
        # Salva o estado da janela
        is_zoomed = self.master.winfo_toplevel().state() == 'zoomed'
        geometry = self.master.geometry()
        
        self.destroy()
        CadastroView(self.master)
        
        # Restaura o estado anterior
        if is_zoomed:
            self.master.state('zoomed')
        else:
            self.master.state('normal')
            self.master.geometry(geometry)
    
    def _abrir_gerenciador(self):
        from views.gerenciador_view import GerenciadorView
        # Salva o estado da janela
        is_zoomed = self.master.winfo_toplevel().state() == 'zoomed'
        geometry = self.master.geometry()
        
        self.destroy()
        GerenciadorView(self.master)
        
        # Restaura o estado anterior
        if is_zoomed:
            self.master.state('zoomed')
        else:
            self.master.state('normal')
            self.master.geometry(geometry)
    
    def _mostrar_erro(self, mensagem):
        MensagemPopup(self, "Erro", mensagem)