import PyInstaller.__main__
import os
import shutil

def limpar_builds_anteriores():
    """Limpa as pastas de build anteriores"""
    pastas_para_limpar = ['dist', 'build', '__pycache__']
    for pasta in pastas_para_limpar:
        if os.path.exists(pasta):
            try:
                shutil.rmtree(pasta)
                print(f"Pasta {pasta} removida com sucesso!")
            except Exception as e:
                print(f"Erro ao remover pasta {pasta}: {str(e)}")
    
    # Remover arquivo .spec se existir
    if os.path.exists('Felichia.spec'):
        try:
            os.remove('Felichia.spec')
            print("Arquivo .spec removido com sucesso!")
        except Exception as e:
            print(f"Erro ao remover arquivo .spec: {str(e)}")

# Limpar builds anteriores
print("Limpando builds anteriores...")
limpar_builds_anteriores()

# Lista de arquivos e pastas para incluir
added_files = [
    ('assets', 'assets'),  # (origem, destino)
    ('views', 'views'),
    ('utils', 'utils'),
    ('data', 'data'),
    ('logs', 'logs')
]

print("Iniciando nova build...")

# Configurações do PyInstaller
PyInstaller.__main__.run([
    'main.py',  # Seu arquivo principal
    '--name=Felichia',  # Nome do executável alterado para Felichia
    '--onefile',  # Criar um único arquivo
    '--windowed',  # Não mostrar console
    '--icon=assets/icones/felichia.ico',  # Ícone do executável
    '--add-data=assets;assets',  # Incluir pasta assets
    '--add-data=views;views',  # Incluir pasta views
    '--add-data=utils;utils',  # Incluir pasta utils
    '--add-data=data;data',  # Incluir pasta data
    '--add-data=logs;logs',  # Incluir pasta logs
    '--clean',  # Limpar cache antes de buildar
    '--noconsole',  # Não mostrar console
    '--noupx',  # Desabilita UPX para evitar falsos positivos em antivírus
    '--noconfirm',  # Sobrescreve arquivos existentes sem perguntar
]) 

print("Build concluída com sucesso!")