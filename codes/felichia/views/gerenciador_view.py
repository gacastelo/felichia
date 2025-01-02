import customtkinter as ctk
from views.popups.adicionar_senha import AdicionarSenhaPopup
from views.popups.alterar_senha import AlterarSenhaPopup
from views.popups.trocar_tema import TrocarTemaPopup
from views.popups.backup import BackupPopup
from controllers.senha_controller import SenhaController
import pyperclip
import logging
from views.base_view import BaseView
from views.popups.mensagem_popup import MensagemPopup
from datetime import datetime, timedelta

class GerenciadorView(BaseView):
    def __init__(self, master):
        super().__init__(master)
        self.senha_controller = SenhaController(self.master.auth_controller.usuario_atual.id)
        self.senhas_selecionadas = []
        self.logger = logging.getLogger('gerenciador_view')
        self.popup_atual = None
        # Atualiza o título da janela
        self.master.title("Felichia - Gerenciamento de Senhas")
        self._criar_widgets()
        self._atualizar_lista()
        
        # Inicia verificação periódica de sessão
        self._verificar_sessao()
    
    def _criar_widgets(self):
        # Frame superior para título e pesquisa
        frame_superior = ctk.CTkFrame(self, fg_color="transparent")
        frame_superior.pack(fill="x", padx=20, pady=10)
        
        # Título
        titulo = ctk.CTkLabel(
            frame_superior,
            text="GERENCIAMENTO DE SENHAS",
            font=("Roboto", 24, "bold")
            
        )
        titulo.pack(side="left", pady=10)
        
        # Frame de pesquisa
        frame_pesquisa = ctk.CTkFrame(self, fg_color="transparent")
        frame_pesquisa.pack(fill="x", padx=20, pady=5)
        
        # Campo de pesquisa
        self.pesquisa_entry = ctk.CTkEntry(
            frame_pesquisa,
            placeholder_text="Pesquisar por site ou usuário...",
            width=300,
            placeholder_text_color="#8E7CC3",  # Roxo suave para o placeholder
            text_color="#8E7CC3",  # Mesma cor para o texto digitado
            border_color="#8E7CC3"  # Opcional: borda também na mesma cor
        )
        self.pesquisa_entry.pack(side="left", padx=5)
        self.pesquisa_entry.bind("<KeyRelease>", self._filtrar_senhas)
        
        # Frame para botões de ação
        frame_acoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_acoes.pack(fill="x", padx=20, pady=5)
        
        # Botões de ação
        botoes = [
            ("Adicionar", self._abrir_adicionar, "#8E7CC3"),  # roxinho fofo
            ("Remover", self._remover_senha, "#8E7CC3"),      # roxinho fofo
            ("Alterar", self._abrir_alterar, "#8E7CC3"),      # roxinho fofo
            ("Atualizar", self._atualizar_lista, "#8E7CC3"),  # roxinho fofo
            ("Copiar Senha", lambda: self._copiar_dado('senha'), "#8E7CC3"),  # roxinho fofo
            ("Copiar Usuário", lambda: self._copiar_dado('usuario'), "#8E7CC3"),  # roxinho fofo
            ("Backup", self._abrir_backup, "#8E7CC3"),  # roxinho fofo           
            ("Temas", self._abrir_temas, "#8E7CC3"),  # roxinho fofo              
            ("Voltar", self._voltar_login, "#8E7CC3")  # roxinho fofo
        ]
        
        for texto, comando, cor in botoes:
            btn = ctk.CTkButton(
                frame_acoes,
                text=texto,
                command=comando,
                width=100,
                fg_color=cor,
                hover_color="#7667a3"  # roxinho fofo mais escuro
            )
            btn.pack(side="left", padx=5)
        
        # Frame para a tabela de senhas
        self.frame_tabela = ctk.CTkFrame(self)
        self.frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Criar cabeçalho da tabela
        self._criar_cabecalho()
        
        # Frame para lista de senhas
        self.frame_lista = ctk.CTkScrollableFrame(self.frame_tabela)
        self.frame_lista.pack(fill="both", expand=True)
    
    def _criar_cabecalho(self):
        frame_header = ctk.CTkFrame(self.frame_tabela, height=30, fg_color="transparent")
        frame_header.pack(fill="x", padx=5, pady=(5,0))
        frame_header.pack_propagate(False)
        
        # Frames com largura fixa e altura reduzida
        frame_site = ctk.CTkFrame(frame_header, fg_color="transparent", width=200)
        frame_site.pack(side="left", padx=2)
        frame_site.pack_propagate(False)
        
        frame_usuario = ctk.CTkFrame(frame_header, fg_color="transparent", width=200)
        frame_usuario.pack(side="left", padx=2)
        frame_usuario.pack_propagate(False)
        
        frame_data = ctk.CTkFrame(frame_header, fg_color="transparent", width=200)
        frame_data.pack(side="right", padx=2)
        frame_data.pack_propagate(False)
        
        # Labels com fonte menor
        ctk.CTkLabel(
            frame_site,
            text="Site",
            font=("Roboto", 12, "bold"),
            anchor="w"
        ).pack(side="left", padx=5)
        
        ctk.CTkLabel(
            frame_usuario,
            text="Usuário",
            font=("Roboto", 12, "bold"),
            anchor="w"
        ).pack(side="left", padx=5)
        
        ctk.CTkLabel(
            frame_data,
            text="Última Modificação",
            font=("Roboto", 12, "bold"),
            anchor="w"
        ).pack(side="left", padx=5)
    
    def _criar_item_senha(self, senha, frame):
        frame_item = ctk.CTkFrame(frame, height=25)
        frame_item.pack(fill="x", padx=5, pady=1)
        frame_item.pack_propagate(False)
        
        # Site
        frame_site = ctk.CTkFrame(frame_item, fg_color="transparent", width=200)
        frame_site.pack(side="left", padx=2)
        frame_site.pack_propagate(False)
        
        label_site = ctk.CTkLabel(
            frame_site,
            text=senha.site,
            anchor="w",
            font=("Roboto", 11)
        )
        label_site.pack(side="left", padx=5)
        
        # Usuário
        frame_usuario = ctk.CTkFrame(frame_item, fg_color="transparent", width=200)
        frame_usuario.pack(side="left", padx=2)
        frame_usuario.pack_propagate(False)
        
        label_usuario = ctk.CTkLabel(
            frame_usuario,
            text=senha.username or "",
            anchor="w",
            font=("Roboto", 11)
        )
        label_usuario.pack(side="left", padx=5)
        
        # Data
        frame_data = ctk.CTkFrame(frame_item, fg_color="transparent", width=200)
        frame_data.pack(side="right", padx=2)
        frame_data.pack_propagate(False)
        
        data_formatada = self._formatar_data(senha.data_modificacao)
        label_data = ctk.CTkLabel(
            frame_data,
            text=data_formatada,
            anchor="w",
            font=("Roboto", 11)
        )
        label_data.pack(side="left", padx=5)
        
        # Bind de clique
        for widget in [frame_item, frame_site, frame_usuario, frame_data,
                      label_site, label_usuario, label_data]:
            widget.bind("<Button-1>", lambda e, s=senha, f=frame_item: self._selecionar_item(s, f))
    
    def _selecionar_item(self, senha, frame):
        if senha in self.senhas_selecionadas:
            self.senhas_selecionadas.remove(senha)
            frame.configure(fg_color=("gray90", "gray13"))
        else:
            self.senhas_selecionadas = [senha]  # Seleciona apenas um
            for child in self.frame_lista.winfo_children():
                child.configure(fg_color=("gray90", "gray13"))
            frame.configure(fg_color=("gray70", "gray30"))
    
    def _atualizar_lista(self):
        try:
            # Limpa a seleção atual
            self.senhas_selecionadas = []
            
            # Busca as senhas antes de limpar a lista atual
            sucesso, resultado = self.senha_controller.listar_senhas()
            
            if not sucesso:
                self._mostrar_erro("Erro ao carregar senhas")
                self.logger.error("Falha ao buscar senhas do banco de dados")
                return
                
            # Se a busca foi bem sucedida, então limpa e atualiza a lista
            for widget in self.frame_lista.winfo_children():
                widget.destroy()
            
            # Limpa o campo de pesquisa
            self.pesquisa_entry.delete(0, 'end')
            
            # Exibe as senhas
            if resultado:  # Verifica se há senhas para exibir
                for senha in resultado:
                    self._criar_item_senha(senha, self.frame_lista)
                self.logger.info(f"Lista atualizada com {len(resultado)} senhas")
            else:
                # Se não houver senhas, exibe uma mensagem na lista
                label = ctk.CTkLabel(
                    self.frame_lista,
                    text="Nenhuma senha cadastrada",
                    font=("Roboto", 12),
                    anchor="center"
                )
                label.pack(pady=20)
                self.logger.info("Lista atualizada - nenhuma senha encontrada")
                
        except Exception as e:
            self.logger.error(f"Erro ao atualizar lista: {str(e)}")
            self._mostrar_erro(f"Erro ao atualizar lista: {str(e)}")
    
    def _filtrar_senhas(self, event=None):
        try:
            filtro = self.pesquisa_entry.get()
            sucesso, resultado = self.senha_controller.listar_senhas(filtro)
            
            # Limpa a lista atual
            for widget in self.frame_lista.winfo_children():
                widget.destroy()
            
            # Exibe resultados filtrados
            if sucesso:
                for senha in resultado:
                    self._criar_item_senha(senha, self.frame_lista)
                
        except Exception as e:
            self.logger.error(f"Erro ao filtrar senhas: {str(e)}")
            self._mostrar_erro("Erro ao filtrar senhas")
    
    def _copiar_dado(self, tipo):
        if not self.senhas_selecionadas:
            self._mostrar_erro("Selecione uma senha primeiro!")
            return
        
        try:
            senha = self.senhas_selecionadas[0]
            if tipo == 'senha':
                pyperclip.copy(senha.senha)
            else:
                pyperclip.copy(senha.username or '')
            
            self._mostrar_sucesso(f"{tipo.title()} copiado para a área de transferência!")
            self.logger.info(f"{tipo.title()} copiado para área de transferência")
            
        except Exception as e:
            self.logger.error(f"Erro ao copiar {tipo}: {str(e)}")
            self._mostrar_erro(f"Erro ao copiar {tipo}")
    
    def _abrir_adicionar(self):
        if self.popup_atual:
            self.popup_atual.destroy()
        self.popup_atual = AdicionarSenhaPopup(self)
    
    def _remover_senha(self):
        if not self.senhas_selecionadas:
            self._mostrar_erro("Selecione uma senha para remover!")
            return
        
        try:
            senha = self.senhas_selecionadas[0]
            sucesso, mensagem = self.senha_controller.remover_senha(senha.id)
            
            if sucesso:
                self._mostrar_sucesso(mensagem)
                self._atualizar_lista()
            else:
                self._mostrar_erro(mensagem)
                
        except Exception as e:
            self.logger.error(f"Erro ao remover senha: {str(e)}")
            self._mostrar_erro("Erro ao remover senha")
    
    def _abrir_alterar(self):
        if not self.senhas_selecionadas:
            self._mostrar_erro("Selecione uma senha para alterar!")
            return
        
        if self.popup_atual:
            self.popup_atual.destroy()
        self.popup_atual = AlterarSenhaPopup(self, self.senhas_selecionadas[0])
    
    def _abrir_backup(self):
        if self.popup_atual:
            self.popup_atual.destroy()
        self.popup_atual = BackupPopup(self)
    
    def _abrir_temas(self):
        if self.popup_atual:
            self.popup_atual.destroy()
        self.popup_atual = TrocarTemaPopup(self)
    
    def _voltar_login(self):
        from views.login_view import LoginView
        # Salva o estado da janela
        is_zoomed = self.master.winfo_toplevel().state() == 'zoomed'
        geometry = self.master.geometry()
        
        self.master.auth_controller.logout()
        self.destroy()
        LoginView(self.master)
        
        # Restaura o estado anterior
        if is_zoomed:
            self.master.state('zoomed')
        else:
            self.master.state('normal')
            self.master.geometry(geometry)
    
    def _verificar_sessao(self):
        """Verifica periodicamente se a sessão ainda está ativa"""
        if not self.master.auth_controller.verificar_sessao_ativa():
            self._voltar_login()
            return
        
        # Agenda próxima verificação em 1 minuto
        self.after(60000, self._verificar_sessao)
    
    def _mostrar_erro(self, mensagem):
        MensagemPopup(self, "Erro", mensagem)
    
    def _mostrar_sucesso(self, mensagem):
        MensagemPopup(self, "Sucesso", mensagem)

    def _formatar_data(self, timestamp):
        try:
            # Se timestamp for datetime, converta diretamente
            if isinstance(timestamp, datetime):
                return timestamp.strftime("%d/%m/%Y %H:%M")
        
            # Se for uma string, remova espaços extras
            timestamp_str = str(timestamp).strip()

            # Tenta fazer o parse da data com microssegundos
            try:
                data = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                # Caso falhe, tenta sem microssegundos
                data = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                data -= timedelta(hours=3)

            # Formata a data para o padrão brasileiro
            return data.strftime("%d/%m/%Y %H:%M")
    
        except Exception as e:
            # Se algo falhar, retorna o timestamp original
            return str(timestamp)