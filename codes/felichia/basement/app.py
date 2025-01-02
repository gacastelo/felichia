import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurações iniciais da janela
        self.title("Gerenciador de Senhas")
        self.geometry("800x600")
        
        # Configuração do tema padrão
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Estado do fullscreen
        self.fullscreen = False
        
        # Bind para teclas de atalho
        self.bind("<F11>", self._alternar_tela_cheia)
        self.bind("<Escape>", self._sair_tela_cheia)
    
    def _alternar_tela_cheia(self, event=None):
        """Alterna entre tela cheia e normal"""
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)
    
    def _sair_tela_cheia(self, event=None):
        """Sai do modo tela cheia"""
        self.fullscreen = False
        self.attributes("-fullscreen", False) 