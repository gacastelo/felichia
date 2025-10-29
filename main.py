from controllers.authController import AuthController
from controllers.credencialController import CredencialController
from controllers.tagController import TagController
from core.database import Database

if __name__ == "__main__":
    db = Database()
    db.setup()
    AuthController = AuthController()
    CredencialController = CredencialController()
    TagController = TagController()
    user_id = None
    chave = None
    while not user_id:
        opcao = int(input("Digite 1 para cadastro, 2 para login: "))
        match opcao:
            case 1:
                AuthController.cadastro("Gabriel", "12345")
            case 2:
                user_id, chave = AuthController.login("Gabriel", "12345")
            case 3:
                break
    while user_id:
        opcao = int(input("Digite 1 para salvar credencial, 2 para listar credenciais: "))
        match opcao:
            case 1:
                CredencialController.salvar_credencial(user_id, chave, "Titulo", "Login", "Site", "Senha", "Tags")
            case 2:
                CredencialController.listar_credenciais(user_id, chave)
            case 3:
                TagController.salvar_tag(user_id, "Tags")
            case 4:
                print(TagController.get_by_title("Tags"))
            case 5:
                TagController.listar_tags(user_id)
            case 6:
                TagController.deletar_tag(user_id)
            case 7:
                TagController.get_by_id(user_id)
            case 9:
                break