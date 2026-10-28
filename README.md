Interface Gráfica

Aplicativo de onboarding feito em Python com CustomTkinter. A interface conduz o usuário pela configuração inicial de um espaço de trabalho em três etapas.

## Funcionalidades
- Criar uma conta e entrar com e-mail e senha.
- Validar campos obrigatórios, formato básico do e-mail e senha com pelo menos 8 caracteres.
- Selecionar ferramentas como Google Drive, GitHub, Slack e Notion.
- Personalizar o nome do espaço, a cor de destaque e o layout.
- Ver um resumo das escolhas e reiniciar o fluxo.

Requisitos
- Python 3.10 ou superior
- CustomTkinter

## Como executar
1. Instale a dependência:
   pip install customtkinter
2. Execute o arquivo:
   python interface_gráfica.py
Se o arquivo tiver outro nome, substitua `interface_gráfica.py` pelo nome correto.

## Observação
Este projeto demonstra uma interface e um fluxo de configuração. As contas e preferências ficam somente na memória durante a execução. Os botões de Google e GitHub e as opções de ferramentas são elementos visuais/interativos da demonstração; não fazem autenticação nem conectam a serviços externos.
