import sqlite3
import zipfile
import json
from datetime import datetime
from pathlib import Path
import shutil
import logging
from utils.database import Database
from tkinter import filedialog
import os

class BackupService:
    def __init__(self):
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
        self.db_path = Path("data/senhas.db")
        self.setup_logging()
    
    def setup_logging(self):
        """Configura o sistema de logging"""
        self.logger = logging.getLogger('backup_service')
        self.logger.setLevel(logging.INFO)
        
        log_file = Path("logs/backup.log")
        log_file.parent.mkdir(exist_ok=True)
        
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)
    
    def criar_backup(self, usuario_id=None):
        """Cria um backup do banco de dados"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"backup_{timestamp}"
            backup_path.mkdir(exist_ok=True)
            
            backup_db = backup_path / "senhas.db"
            
            with sqlite3.connect(self.db_path) as src, \
                 sqlite3.connect(backup_db) as dst:
                src.backup(dst)
            
            self._exportar_json(backup_path, usuario_id)
            
            zip_path = self.backup_dir / f"backup_{timestamp}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in backup_path.rglob('*'):
                    zipf.write(file, file.relative_to(backup_path))
            
            shutil.rmtree(backup_path)
            
            self.logger.info(f"Backup criado com sucesso: {zip_path}")
            self._manter_apenas_ultimos_backups()
            
            return True, f"Backup criado com sucesso: {zip_path}"
        
        except Exception as e:
            self.logger.error(f"Erro ao criar backup: {str(e)}")
            return False, f"Erro ao criar backup: {str(e)}"
    
    def importar_backup(self, usuario_id):
        """Importa um backup JSON para o banco de dados"""
        try:
            filename = filedialog.askopenfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")]
            )
            
            if not filename:
                return False, "Operação cancelada"
            
            with open(filename, 'r', encoding='utf-8') as f:
                dados_backup = json.load(f)
            
            if "usuario" not in dados_backup or "senhas" not in dados_backup:
                return False, "Formato de backup inválido"
            
            if dados_backup["usuario"].get("id") != usuario_id:
                return False, "Este backup pertence a outro usuário"
            
            db = Database()
            with db.conectar() as conn:
                cursor = conn.cursor()
                
                for senha in dados_backup["senhas"]:
                    try:
                        cursor.execute(
                            "SELECT id FROM senhas WHERE id = ? AND usuario_id = ?",
                            (senha["id"], usuario_id)
                        )
                        resultado = cursor.fetchone()
                        
                        if resultado:
                            cursor.execute("""
                                UPDATE senhas 
                                SET site = ?, username = ?, senha_criptografada = ?,
                                    data_modificacao = CURRENT_TIMESTAMP
                                WHERE id = ? AND usuario_id = ?
                            """, (
                                senha["site"], senha["username"], senha["senha_criptografada"],
                                senha["id"], usuario_id
                            ))
                        else:
                            cursor.execute("""
                                INSERT INTO senhas (site, usuario_id, username, senha_criptografada)
                                VALUES (?, ?, ?, ?)
                            """, (
                                senha["site"], usuario_id, senha["username"], senha["senha_criptografada"]
                            ))
                    except Exception as e:
                        self.logger.error(f"Erro ao processar senha {senha}: {str(e)}")
                
                conn.commit()
            
            return True, "Backup importado com sucesso!"
            
        except Exception as e:
            self.logger.error(f"Erro ao importar backup: {str(e)}")
            return False, f"Erro ao importar backup: {str(e)}"

    def _exportar_json(self, backup_path, usuario_id=None):
        """Exporta os dados em formato JSON"""
        db = Database()
        with db.conectar() as conn:
            cursor = conn.cursor()
            
            if usuario_id:
                cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
            else:
                cursor.execute("SELECT * FROM usuarios")
            usuarios = cursor.fetchall()
            
            if usuario_id:
                cursor.execute("SELECT * FROM senhas WHERE usuario_id = ?", (usuario_id,))
            else:
                cursor.execute("SELECT * FROM senhas")
            senhas = cursor.fetchall()
            
            dados = {
                "usuarios": usuarios,
                "senhas": senhas
            }
            
            json_path = backup_path / "dados.json"
            with open(json_path, 'w') as f:
                json.dump(dados, f, indent=4, default=str)

    def _manter_apenas_ultimos_backups(self, max_backups=5):
        """Mantém apenas os últimos N backups"""
        backups = sorted(
            self.backup_dir.glob("*.zip"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        for backup in backups[max_backups:]:
            backup.unlink()
            self.logger.info(f"Backup antigo removido: {backup}")

    