#Gerenciador de Senhas

Interface gráfica unsando customtkinter

TELA INICIAL
        TITULO: LOGIN
        SUBTITULO: Informe seu nome de usuário e senha para continuar
        ENTRADA PARA NOME DE USUÁRIO: Campo para inserir o nome de usuário
        ENTRADA PARA SENHA: Campo para inserir a senha
        BOTÃO PARA CADASTRAR: Botão para cadastrar um novo usuário
        BOTÃO PARA SAIR: Botão para sair do aplicativo

TELA DE CADASTRO
	ELEMENTOS
        TITULO: CADASTRO
        SUBTITULO: Crie seu nome de usuário e senha para continuar
        ENTRADA PARA NOME DE USUÁRIO: Campo para inserir o nome de usuário
        ENTRADA PARA SENHA: Campo para inserir a senha
        BOTÃO PARA CADASTRAR: Botão para cadastrar o usuário
        BOTÃO PARA VOLTAR: Botão para voltar para a tela de login

TELA DE GERENCIAMENTO DE SENHAS
	ELEMENTOS
        TITULO: GERENCIAMENTO DE SENHAS
        FILTRO PARA PESQUISAR SENHAS POR NOME DO SITE OU USUÁRIO
        TABELA PARA MOSTRAR AS SENHAS CADASTRADAS
        BOTÃO PARA VOLTAR: Botão para voltar para a tela inicial
        BOTÃO PARA ADICIONAR: Botão para adicionar uma nova senha(abrir um pop-up para adicionar o site, o usuario e a senha)
        BOTÃO PARA REMOVER: Botão para remover uma senha
        BOTÃO PARA ATUALIZAR: Botão para atualizar a lista de senhas
        BOTÃO PARA ALTERAR: Botão para alterar uma senha(abrir um pop-up para alterar o site, o usuario e a senha)
        BOTÃO PARA COPIAR: Botão para copiar a senha ou o usuario para a área de transferência(pyperclip)
        TROCAR TEMAS: Botão para trocar o tema do aplicativo(popup customtkinter)

POP-UP PARA ADICIONAR SENHA
	ELEMENTOS
        ENTRADA PARA SITE: Campo para inserir o nome do site
        ENTRADA PARA USUÁRIO: Campo para inserir o nome de usuário(não é obrigatório)
        ENTRADA PARA SENHA: Campo para inserir a senha(criptografada com base na senha mestra ou cryptography)
        BOTÃO PARA SALVAR: Botão para salvar a nova senha
        BOTÃO PARA CANCELAR: Botão para cancelar a operação e fechar o pop-up

POP-UP PARA ALTERAR SENHA
	ELEMENTOS
        ENTRADA PARA SITE: Campo para inserir o nome do site(caso este esteja vazio permanecer o mesmo)
        ENTRADA PARA USUÁRIO: Campo para inserir o nome de usuário(não é obrigatório)(caso este esteja vazio permanecer o mesmo)
        ENTRADA PARA SENHA: Campo para inserir a senha(caso este esteja vazio permanecer o mesmo)
        BOTÃO PARA SALVAR: Botão para salvar a alteração da senha
        BOTÃO PARA CANCELAR: Botão para cancelar a operação e fechar o pop-up

POP-UP PARA TROCAR TEMAS
	ELEMENTOS
        BOTÃO PARA TROCAR: Botão para trocar o tema do aplicativo(poder trocar entre light e dark e superdark, além de poder escolher uma paleta de cores, e salvar a paleta escolhida)
        BOTÃO PARA CANCELAR: Botão para cancelar a operação e fechar o pop-up

ESTRUTURA DE FUNCIONAMENTO
    A senha mestra é armazenada em um arquivo .hash
    A senha é criptografada com base na senha mestra
    A senha é armazenada em um arquivo .db SQLite
    A senha é descriptografada com base na senha mestra
    Caso passe de 5 dias sem acessar o aplicativo a senha mestra é requisitada novamente
    A senha mestra pode ser alterada a qualquer momento pelo usuário administrador
    Após 15 minutos de inatividade o usuário é desconectado do aplicativo
    O usuário pode ser excluido a qualquer momento pelo usuário administrador

EXEMPLO DE ESTRUTURA DO PROJETO
projeto/
├── main.py
├── views/
│   ├── login_view.py
│   ├── cadastro_view.py
│   ├── gerenciador_view.py
│   └── popups/
│       ├── adicionar_senha.py
│       └── alterar_senha.py
├── models/
│   ├── usuario.py
│   └── senha.py
├── controllers/
│   ├── auth_controller.py
│   └── senha_controller.py
└── utils/
    ├── database.py
    └── criptografia.py

EXEMPLO DE ESTRUTURA DO BANCO DE DADOS

-- Tabela de Usuários (administradores do sistema)
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultimo_acesso DATETIME,
    is_admin BOOLEAN DEFAULT 0
);

-- Tabela de Senhas Armazenadas
CREATE TABLE senhas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    site TEXT NOT NULL,
    username TEXT,
    senha_criptografada TEXT NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_modificacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabela de Logs de Acesso
CREATE TABLE logs_acesso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    acao TEXT NOT NULL,
    ip TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabela de Configurações
CREATE TABLE configuracoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    tempo_sessao INTEGER DEFAULT 900, -- 15 minutos em segundos
    tempo_expiracao_senha INTEGER DEFAULT 432000, -- 5 dias em segundos
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

RECURSOS ADICIONAIS
    SEGURANÇA ADICIONAL:

    -- Adicionar à tabela usuarios
ALTER TABLE usuarios ADD COLUMN tentativas_login INTEGER DEFAULT 0;
ALTER TABLE usuarios ADD COLUMN bloqueado_ate DATETIME;
ALTER TABLE usuarios ADD COLUMN ultima_troca_senha DATETIME;

-- Nova tabela para histórico de senhas
CREATE TABLE historico_senhas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    senha_id INTEGER NOT NULL,
    senha_antiga TEXT NOT NULL,
    data_modificacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    modificado_por INTEGER NOT NULL,
    FOREIGN KEY (senha_id) REFERENCES senhas(id),
    FOREIGN KEY (modificado_por) REFERENCES usuarios(id)
);

-- Nova tabela para categorias de senhas
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    cor TEXT
);

Melhorias na Estrutura de Código
class SenhaManager:
    def __init__(self):
        self.crypto = CriptografiaService()
        self.db = Database()
    
    def gerar_senha_forte(self, tamanho=16):
        """Gera uma senha forte aleatória"""
        caracteres = string.ascii_letters + string.digits + string.punctuation
        while True:
            senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
            if (any(c.islower() for c in senha)
                    and any(c.isupper() for c in senha)
                    and any(c.isdigit() for c in senha)
                    and any(c in string.punctuation for c in senha)):
                return senha
    
    def verificar_força_senha(self, senha):
        """Verifica a força da senha"""
        pontuacao = 0
        checks = {
            'comprimento': len(senha) >= 8,
            'maiuscula': any(c.isupper() for c in senha),
            'minuscula': any(c.islower() for c in senha),
            'numeros': any(c.isdigit() for c in senha),
            'especiais': any(c in string.punctuation for c in senha)
        }
        return checks
Sistema de Backup Automático
class BackupService:
    def __init__(self):
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    def criar_backup(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"backup_{timestamp}.db"
        
        with sqlite3.connect("senhas.db") as src, \
             sqlite3.connect(backup_file) as dst:
            src.backup(dst)
        
        # Compactar backup
        with zipfile.ZipFile(f"{backup_file}.zip", 'w') as zip_file:
            zip_file.write(backup_file, arcname=backup_file.name)

Sistema de Notificações
class NotificacaoService:
    def __init__(self):
        self.notificacoes = []
    
    def adicionar_notificacao(self, usuario_id, tipo, mensagem):
        with Database().conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO notificacoes (usuario_id, tipo, mensagem)
                VALUES (?, ?, ?)
            ''', (usuario_id, tipo, mensagem))
    
    def get_notificacoes_pendentes(self, usuario_id):
        with Database().conectar() as conn:
            cursor = conn.cursor()
            return cursor.execute('''
                SELECT * FROM notificacoes 
                WHERE usuario_id = ? AND lida = 0
            ''', (usuario_id,)).fetchall()

Melhorias na Interface
class TelaGerenciador(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        # Adicionar barra de pesquisa avançada
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(fill="x", padx=10, pady=5)
        
        self.search_entry = ctk.CTkEntry(self.search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True)
        
        self.category_combobox = ctk.CTkComboBox(
            self.search_frame,
            values=["Todas", "Email", "Banco", "Trabalho", "Pessoal"]
        )
        self.category_combobox.pack(side="left", padx=5)

Sistema de Exportação/Importação
class ExportService:
    def exportar_csv(self, usuario_id, caminho):
        with Database().conectar() as conn:
            cursor = conn.cursor()
            senhas = cursor.execute('''
                SELECT site, username, senha_criptografada 
                FROM senhas WHERE usuario_id = ?
            ''', (usuario_id,)).fetchall()
            
            with open(caminho, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Site', 'Usuário', 'Senha'])
                for senha in senhas:
                    writer.writerow(senha)

Logging Avançado
import logging
from logging.handlers import RotatingFileHandler

def configurar_logging():
    logger = logging.getLogger('gerenciador_senhas')
    logger.setLevel(logging.INFO)
    
    handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=1024*1024,  # 1MB
        backupCount=5
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    Configurações Avançadas

class ConfiguracoesAvancadas:
    def __init__(self):
        self.config = {
            'tempo_sessao': 900,  # 15 minutos
            'tempo_expiracao_senha': 432000,  # 5 dias
            'max_tentativas_login': 3,
            'tempo_bloqueio': 1800,  # 30 minutos
            'tamanho_minimo_senha': 8,
            'backup_automatico': True,
            'intervalo_backup': 86400,  # 1 dia
            'tema': 'dark',
            'fonte': 'Roboto',
            'tamanho_fonte': 12
        }

