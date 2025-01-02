from views.popups.base_popup import BasePopup
import customtkinter as ctk
from tkinter import messagebox
from tkinter import filedialog
import shutil
import os

class BackupPopup(BasePopup):
    def __init__(self, master):
        super().__init__(master, "Backup", 400, 300)
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Frame principal
        frame = ctk.CTkFrame(self)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Botões
        btn_exportar = ctk.CTkButton(
            frame, 
            text="Exportar Backup", 
            command=self._exportar,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_exportar.pack(pady=10)
        
        btn_importar = ctk.CTkButton(
            frame, 
            text="Importar Backup", 
            command=self._importar,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_importar.pack(pady=10)
        
        btn_fechar = ctk.CTkButton(
            frame, 
            text="Fechar", 
            command=self.destroy,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_fechar.pack(pady=10)

        btn_chave = ctk.CTkButton(
            frame, 
            text="Baixar Chave", 
            command=self.baixar_chave,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_chave.pack(pady=10)
    
    def _exportar(self):
        sucesso, mensagem = self.master.master.backup_service.exportar_backup(
            self.master.master.auth_controller.usuario_atual.id
        )
        
        if sucesso:
            self.master._mostrar_sucesso(mensagem)
        else:
            self.master._mostrar_erro(mensagem)
    
    def _importar(self):
        sucesso, mensagem = self.master.master.backup_service.importar_backup(
            self.master.master.auth_controller.usuario_atual.id
        )
        
        if sucesso:
            self.master._mostrar_sucesso(mensagem)
            self.master._atualizar_lista()
        else:
            self.master._mostrar_erro(mensagem)

    # Método para baixar a chave
    def baixar_chave(self):
        try:
            # Mensagem inicial
            messagebox.showinfo(
                "Informação", 
                "A chave é usada para recuperar seu backup em outra máquina. Clique em OK para continuar."
            )

            # Abre o explorer para selecionar a pasta
            pasta_destino = filedialog.askdirectory(
                title="Selecione a pasta para salvar a chave"
            )

            if not pasta_destino:  # Se o usuário cancelar
                messagebox.showwarning("Cancelado", "Operação cancelada.")
                return

            # Caminho da chave original
            chave_origem = os.path.join("data", "chave.key")

            # Verifica se o arquivo existe
            if not os.path.exists(chave_origem):
                messagebox.showerror(
                    "Erro", 
                    "O arquivo da chave não foi encontrado. Verifique o diretório 'data'."
                )
                return

            # Caminho do destino
            chave_destino = os.path.join(pasta_destino, "chave.key")

            # Copia a chave para o destino
            shutil.copy(chave_origem, chave_destino)

            # Confirmação de sucesso
            messagebox.showinfo(
                "Sucesso", 
                f"A chave foi salva em: {chave_destino}"
            )
        except Exception as e:
            # Log e mensagem de erro
            self.logger.error(f"Erro ao baixar a chave: {str(e)}")
            messagebox.showerror(
                "Erro", 
                f"Ocorreu um erro ao baixar a chave: {str(e)}"
            )