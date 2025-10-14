Bot de Encaminhamento Telegram para Discord
Um bot de desktop com interface gráfica que monitora mensagens e imagens de um canal específico do Telegram (público ou privado) e as encaminha em tempo real para um canal do Discord através de um Webhook.

O programa foi desenvolvido em Python com uma interface amigável usando Tkinter e pode ser minimizado para a bandeja do sistema (próximo ao relógio do Windows), rodando em segundo plano.

Funcionalidades
Interface Gráfica Simples: Configure todas as suas credenciais e informações em uma janela fácil de usar.

Monitoramento em Tempo Real: Captura novas mensagens assim que são publicadas no canal do Telegram.

Encaminhamento de Mídia: Envia não apenas o texto da mensagem, mas também as imagens anexadas.

Operação em Segundo Plano: O programa pode ser minimizado para a bandeja do sistema, continuando a funcionar sem atrapalhar o uso do computador.

Configuração Persistente: Salva suas informações em um arquivo config.json para não precisar digitá-las toda vez que abrir o programa.

Autônomo: Pode ser compilado em um único arquivo executável (.exe) que não requer a instalação do Python para ser executado.

Guia de Instalação e Configuração
Para fazer o bot funcionar, você precisará obter algumas chaves de API. Siga os passos abaixo.

Pré-requisitos
Python 3.8+ instalado em seu computador.

Uma conta no Telegram e uma conta no Discord.

Passo 1: Clonar e Instalar as Dependências
Primeiro, baixe o código e instale as bibliotecas necessárias.

# 1. Clone o repositório para o seu computador
git clone https://github.com/SEU-USUARIO/bot-telegram-discord.git

# 2. Navegue até a pasta do projeto
cd bot-telegram-discord

# 3. (Recomendado) Crie e ative um ambiente virtual
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Mac/Linux:
# source venv/bin/activate

# 4. Instale todas as dependências do projeto
pip install -r requirements.txt

Passo 2: Obter as Credenciais Necessárias
Esta é a parte mais importante. Você precisará de duas chaves do Telegram e uma URL do Discord.

A. Obter TELEGRAM_API_ID e TELEGRAM_API_HASH
Estas chaves identificam sua aplicação para o Telegram.

Faça login com sua conta do Telegram no site oficial: my.telegram.org.

Clique em "API development tools".

Preencha o formulário de criação de aplicativo (os nomes podem ser qualquer coisa):

App title: Meu Bot de Mensagens

Short name: meu_bot_de_msg_ (use um nome único, com letras e números).

Platform: Desktop

Clique em "Create application".

A página seguinte mostrará suas credenciais. Copie e guarde os valores de api_id e api_hash.

B. Obter a DISCORD_WEBHOOK_URL
Esta URL permite que o bot envie mensagens para um canal específico no seu servidor do Discord.

Abra o Discord (no aplicativo ou no navegador).

Clique com o botão direito no canal de texto para onde as mensagens devem ser enviadas.

Vá em Editar canal > Integrações.

Clique em "Criar Webhook".

Dê um nome ao seu Webhook (ex: "Ponte do Telegram") e clique em "Copiar URL do Webhook".

Guarde essa URL. Trate-a como uma senha, não a compartilhe publicamente.

Passo 3: Rodar a Aplicação
Com todas as credenciais em mãos, você pode iniciar o bot.

No terminal, na pasta do projeto, execute o seguinte comando:
python main_gui.py

A interface gráfica do bot será aberta. Preencha todos os campos com as informações que você coletou:

Telegram API ID: Seu api_id.

Telegram API Hash: Seu api_hash.

Nº de Telefone: Seu número do Telegram no formato internacional (ex: +55119...).

Canal para Monitorar: O @username do canal ou grupo público. Para grupos privados, você precisará do ID numérico.

URL Webhook Discord: A URL que você copiou do Discord.

Senha 2 Fatores: Se sua conta do Telegram tiver a verificação em duas etapas ativada, digite a senha aqui. Se não, pode deixar em branco.

Clique em "Salvar Configuração". Isso criará um arquivo config.json para uso futuro.

Clique em "▶ Iniciar Bot".

Na primeira vez que você iniciar, o Telegram enviará um código de login para seu aplicativo. Uma janela pop-up aparecerá no bot para você digitar esse código. Após o login, o bot começará a funcionar.

Usando o Bot em Segundo Plano
Para minimizar o bot, basta clicar no "X" da janela. Ele desaparecerá da barra de tarefas e ficará rodando como um ícone na bandeja do sistema (próximo ao relógio).

Para reabrir a janela, clique com o botão direito no ícone na bandeja e selecione "Mostrar".

Para fechar o programa completamente, clique com o botão direito no ícone e selecione "Sair".
