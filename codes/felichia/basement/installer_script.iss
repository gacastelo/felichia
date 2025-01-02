#define MyAppName "Felichia"
#define MyAppVersion "1.0"
#define MyAppPublisher "Gabriel Castelo"
#define MyAppURL "https://github.com/gacastelo"
#define MyAppExeName "Felichia.exe"

[Setup]
; Configurações básicas
AppId={{8A839397-9B9E-4C84-9041-F69749E0A542}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; Configurações de aparência
WizardStyle=modern
LicenseFile=license.txt
; Local onde será gerado o instalador
OutputDir=installer
OutputBaseFilename=Felichia_Setup
; Compressão
Compression=lzma2/ultra64
SolidCompression=yes
; Ícone do instalador
SetupIconFile=assets\Felichia_logo3.ico
; Requisitos mínimos
MinVersion=10.0
; Privilégios necessários
PrivilegesRequired=admin
; Informações sobre o instalador
VersionInfoDescription=Instalador do Felichia Password Manager
VersionInfoProductName=Felichia Password Manager
VersionInfoCompany=Gabriel Castelo
VersionInfoCopyright=Copyright © 2024 Gabriel Castelo
VersionInfoProductVersion={#MyAppVersion}
VersionInfoVersion={#MyAppVersion}

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Messages]
; Mensagens personalizadas em português
BeveledLabel=Felichia Password Manager
WelcomeLabel1=Bem-vindo ao Assistente de Instalação do Felichia
WelcomeLabel2=Este programa instalará o Felichia Password Manager em seu computador.%n%nO Felichia é um gerenciador de senhas seguro e fácil de usar, desenvolvido para ajudar você a manter suas senhas organizadas e protegidas.%n%nPor favor, leia atentamente os termos da licença na próxima tela antes de prosseguir.%n%nRecomendamos que você feche todos os outros aplicativos antes de continuar.
FinishedLabel=A instalação do Felichia foi concluída com sucesso. O aplicativo pode ser iniciado selecionando o ícone instalado.
LicenseLabel3=Por favor, leia o Contrato de Licença de Uso do Software. Você deve aceitar os termos deste contrato antes de continuar a instalação.

[Tasks]
; Ícone na área de trabalho (marcado por padrão)
Name: "desktopicon"; Description: "Criar ícone na área de trabalho"; GroupDescription: "Ícones adicionais"; Flags: checkedonce

; Fixar no Menu Iniciar (marcado por padrão)
Name: "pintostartmenu"; Description: "Fixar no Menu Iniciar"; GroupDescription: "Ícones adicionais"; Flags: checkedonce

[Files]
; Copia todos os arquivos da pasta dist\Felichia
Source: "dist\Felichia\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
; Ícones normais
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\_internal\assets\Felichia_logo3.ico"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\_internal\assets\Felichia_logo3.ico"; Tasks: desktopicon

; Fixar no Menu Iniciar
Name: "{userprograms}\Windows.Explorer.Pinned\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\_internal\assets\Felichia_logo3.ico"; Tasks: pintostartmenu

[Run]
Filename: "{sys}\cmd.exe"; \
    Parameters: "/c start """" ""{app}\{#MyAppExeName}"""; \
    Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; \
    Flags: nowait postinstall skipifsilent runascurrentuser shellexec

[Registry]
; Força a execução como administrador
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"; \
    ValueType: string; ValueName: "{app}\{#MyAppExeName}"; \
    ValueData: "RUNASADMIN"; \
    Flags: uninsdeletekeyifempty uninsdeletevalue; \
    Check: IsAdminInstallMode