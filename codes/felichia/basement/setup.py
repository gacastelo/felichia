from cx_Freeze import setup, Executable

setup(
    name="Felichia",
    version="1.3",
    description="Gerenciador de Senhas",
    executables=[Executable("main.py", base=None, targetName="felichia.exe")]
)
