import customtkinter as ctk
import re
import shutil
import os
from tkinter import filedialog, messagebox

class CadastroView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Felichia - Cadastro")
        self.pack(fill="both", expand=True)
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Frame central
        frame_central = ctk.CTkFrame(self)
        frame_central.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        titulo = ctk.CTkLabel(
            frame_central,
            text="CADASTRO",
            font=("Roboto", 24, "bold")
        )
        titulo.pack(pady=20)
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(
            frame_central,
            text="Crie seu nome de usuário e senha para continuar",
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
        
        # Campo de confirmação de senha
        self.confirm_password_entry = ctk.CTkEntry(
            frame_central,
            placeholder_text="Confirme a senha",
            show="•",
            width=300
        )
        self.confirm_password_entry.pack(pady=10)
        
        # Indicadores de força da senha
        self.frame_forca = ctk.CTkFrame(frame_central)
        self.frame_forca.pack(pady=10)
        
        self.label_forca = ctk.CTkLabel(
            self.frame_forca,
            text="Força da senha:",
            font=("Roboto", 11)
        )
        self.label_forca.pack(side="left", padx=5)
        
        self.barra_forca = ctk.CTkProgressBar(
            self.frame_forca,
            width=200,
            height=10
        )
        self.barra_forca.pack(side="left", padx=5)
        self.barra_forca.set(0)
        
        # Requisitos da senha
        frame_requisitos = ctk.CTkFrame(frame_central)
        frame_requisitos.pack(pady=5)
        
        requisitos = [
            "Mínimo 8 caracteres",
            "Letra maiúscula",
            "Letra minúscula",
            "Número",
            "Caractere especial"
        ]
        
        self.labels_requisitos = {}
        for req in requisitos:
            label = ctk.CTkLabel(
                frame_requisitos,
                text="✗ " + req,
                font=("Roboto", 10),
                text_color="gray60"
            )
            label.pack(anchor="w", padx=5)
            self.labels_requisitos[req] = label
        
        # Frame para botões
        frame_botoes = ctk.CTkFrame(frame_central, fg_color="transparent")
        frame_botoes.pack(pady=20)
        
        # Botão de cadastrar
        btn_cadastrar = ctk.CTkButton(
            frame_botoes,
            text="Cadastrar",
            command=self._fazer_cadastro,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_cadastrar.pack(side="left", padx=5)
        
        # Botão de voltar
        btn_voltar = ctk.CTkButton(
            frame_botoes,
            text="Voltar",
            command=self._voltar_login,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_voltar.pack(side="left", padx=5)

        # Botão de inserir chave
        btn_voltar = ctk.CTkButton(
            frame_botoes,
            text="Inserir Chave",
            command=self._inserir_chave,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_voltar.pack(side="left", padx=5)
        
        # Bind para verificar força da senha
        self.password_entry.bind("<KeyRelease>", self._verificar_forca_senha)
    
    def _verificar_forca_senha(self, event=None):
        senha = self.password_entry.get()
        pontuacao = 0
        max_pontos = 5
        
        # Verifica cada requisito
        requisitos = {
            "Mínimo 8 caracteres": len(senha) >= 8,
            "Letra maiúscula": bool(re.search(r'[A-Z]', senha)),
            "Letra minúscula": bool(re.search(r'[a-z]', senha)),
            "Número": bool(re.search(r'\d', senha)),
            "Caractere especial": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', senha))
        }
        
        # Atualiza os indicadores visuais
        for req, atende in requisitos.items():
            label = self.labels_requisitos[req]
            if atende:
                label.configure(text="✓ " + req, text_color="green")
                pontuacao += 1
            else:
                label.configure(text="✗ " + req, text_color="gray60")
        
        # Atualiza a barra de progresso
        self.barra_forca.set(pontuacao / max_pontos)
        
        # Define a cor da barra baseado na força
        if pontuacao <= 2:
            self.barra_forca.configure(progress_color="red")
        elif pontuacao <= 3:
            self.barra_forca.configure(progress_color="yellow")
        else:
            self.barra_forca.configure(progress_color="green")
    
    def _fazer_cadastro(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validações básicas
        if not username or not password or not confirm_password:
            self._mostrar_erro("Todos os campos são obrigatórios!")
            return
        
        if password != confirm_password:
            self._mostrar_erro("As senhas não coincidem!")
            return
        
        if len(password) < 8:
            self._mostrar_erro("A senha deve ter pelo menos 8 caracteres!")
            return
        
        # Verifica requisitos mínimos de senha
        if not all([
            re.search(r'[A-Z]', password),
            re.search(r'[a-z]', password),
            re.search(r'\d', password),
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
        ]):
            self._mostrar_erro("A senha não atende aos requisitos mínimos!")
            return
        
        # Tenta cadastrar o usuário
        sucesso, mensagem = self.master.auth_controller.cadastrar(username, password)
        
        if sucesso:
            self._mostrar_sucesso("Cadastro realizado com sucesso!")
            self._voltar_login()
        else:
            self._mostrar_erro(mensagem)
    
    def _voltar_login(self):
        from views.login_view import LoginView
        
        # Primeiro destruímos a view atual
        self.destroy()
        
        # Criamos a nova view de login
        login_view = LoginView(self.master)
        
        # Garantimos que a nova view seja exibida
        login_view.pack(fill="both", expand=True)
        
        # Atualizamos o título da janela
        self.master.title("Felichia - Login")
    
    def _mostrar_erro(self, mensagem):
        from views.popups.mensagem_popup import MensagemPopup
        MensagemPopup(self, "Erro", mensagem)
    
    def _mostrar_sucesso(self, mensagem):
        from views.popups.mensagem_popup import MensagemPopup
        MensagemPopup(self, "Sucesso", mensagem)

    def _inserir_chave(self):
        try:
            # Solicita ao usuário que selecione o arquivo da chave
            arquivo_chave = filedialog.askopenfilename(
                title="Selecione a chave",
                filetypes=[("Arquivo de Chave", "*.key")]
            )
            
            if not arquivo_chave:
                # Se o usuário cancelar
                messagebox.showwarning("Cancelado", "Operação cancelada.")
                return
            
            # Verifica se o arquivo selecionado existe
            if not os.path.exists(arquivo_chave):
                messagebox.showerror("Erro", "O arquivo da chave não foi encontrado.")
                return
            
            # Caminho de destino para a chave
            pasta_destino = os.path.join(os.getcwd(), "data", "chave.key")
            
            # Cria a pasta "data" se ela não existir
            os.makedirs(os.path.dirname(pasta_destino), exist_ok=True)
            
            # Copia a chave para o diretório de destino
            shutil.copy(arquivo_chave, pasta_destino)
            
            # Mensagem de sucesso
            messagebox.showinfo("Sucesso", f"A chave foi inserida em: {pasta_destino}, agora pode prosseguir com seu cadastro para acessar suas senhas")
        
        except Exception as e:
            # Se ocorrer um erro
            messagebox.showerror("Erro", f"Ocorreu um erro ao inserir a chave: {str(e)}")