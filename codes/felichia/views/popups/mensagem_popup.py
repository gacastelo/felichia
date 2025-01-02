import customtkinter as ctk
from .base_popup import BasePopup
import os
from pathlib import Path
import tkinter as tk
import logging

class MensagemPopup(BasePopup):
    def __init__(self, master, titulo, mensagem):
        # Remove a configuração de ícone da classe base temporariamente
        BasePopup._configure_icon = lambda self: None
        
        # Chama o construtor da classe base
        super().__init__(master, titulo, largura=300, altura=150)
        
        # Configura o ícone diretamente
        try:
            if os.name == 'nt':  # Windows
                icon_path = Path(__file__).parent/ "assets" / "icones" / "Felichia_logo.ico"
                self.iconbitmap(str(icon_path))
                self.wm_iconbitmap(str(icon_path))
                # Força o Windows a atualizar o ícone
                self.update_idletasks()
            else:  # Linux/Mac
                icon_path = Path(__file__).parent/ "assets" / "icones" / "felichia_logo2.png"
                icon = tk.PhotoImage(file=str(icon_path))
                self.iconphoto(True, icon)
        except Exception as e:
            logging.error(f"Erro ao definir ícone no MensagemPopup: {e}")
        
        # Frame principal
        self.frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_conteudo.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Label com a mensagem
        label = ctk.CTkLabel(
            self.frame_conteudo,
            text=mensagem,
            font=("Roboto", int(12 * self.escala)),
            wraplength=int(250 * self.escala)
        )
        label.pack(pady=20)
        
        # Botão OK
        btn_ok = ctk.CTkButton(
            self.frame_conteudo,
            text="OK",
            command=self.destroy,
            width=int(100 * self.escala),
            height=int(32 * self.escala),
            font=("Roboto", int(12 * self.escala)),
            fg_color="#8E7CC3",
            hover_color="#7667a3"
        )
        btn_ok.pack(pady=10)
        
        # Restaura o método original da classe base
        delattr(BasePopup, '_configure_icon')