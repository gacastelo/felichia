from PIL import Image
import os

def create_windows_ico(png_path, ico_path):
    """
    Cria um arquivo .ico otimizado para o Windows Explorer
    com todas as resoluções padrão do Windows
    """
    try:
        # Abre a imagem original
        img = Image.open(png_path)
        
        # Tamanhos padrão do Windows Explorer
        windows_sizes = [
            (16, 16),    # Ícone pequeno
            (20, 20),    # Mini ícone
            (24, 24),    # Lista
            (32, 32),    # Ícone grande
            (40, 40),    # Lista extra grande
            (48, 48),    # Ícones médios
            (64, 64),    # Ícones grandes
            (96, 96),    # Super grandes
            (128, 128),  # Jumbo
            (256, 256),  # Full size
            (512, 512)   # Ultra HD
        ]
        
        # Cria as diferentes resoluções
        img_list = []
        for size in windows_sizes:
            # Usa LANCZOS para melhor qualidade
            resized = img.resize(size, Image.Resampling.LANCZOS)
            # Garante que a imagem está em RGBA
            if resized.mode != 'RGBA':
                resized = resized.convert('RGBA')
            img_list.append(resized)
        
        # Salva como .ico com todas as resoluções
        img_list[0].save(
            ico_path, 
            format='ICO',
            sizes=[(img.width, img.height) for img in img_list],
            append_images=img_list[1:],
            quality=100  # Máxima qualidade
        )
        print(f"Arquivo .ico criado com sucesso em: {ico_path}")
        return True
    except Exception as e:
        print(f"Erro ao criar .ico: {e}")
        return False

# Cria o ícone
create_windows_ico(
    'assets/Felichia_logo2.png',  # sua imagem PNG original (use uma de alta resolução)
    'assets/Felichia_logo.ico'   # onde salvar o novo .ico
) 