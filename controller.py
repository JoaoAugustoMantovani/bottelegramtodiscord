import os
import asyncio
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from discord_service import DiscordWebhookService

class TelegramController:
    def __init__(self, config, logger, prompt_callback):
        self.config = config
        self.logger = logger
        self.prompt_callback = prompt_callback 
        self.discord_service = None
        self.client = None
        self.loop = None

    def setup(self):
        try:
            api_id = self.config['TELEGRAM_API_ID']
            api_hash = self.config['TELEGRAM_API_HASH']
            
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

            self.client = TelegramClient('bot_session', api_id, api_hash, loop=self.loop)
            
            webhook_url = self.config['DISCORD_WEBHOOK_URL']
            self.discord_service = DiscordWebhookService(webhook_url)
            return True
        except KeyError as e:
            self.logger.log(f"[ERRO] Chave de configuração ausente: {e}")
            return False
        except Exception as e:
            self.logger.log(f"[ERRO] Falha na configuração inicial: {e}")
            return False
        
    async def _message_handler(self, event):
       
        self.logger.log(f"Nova mensagem recebida do canal: {getattr(event.chat, 'title', event.chat_id)}")
        
        downloaded_image_path = None
        try:
            if event.message.photo:
                self.logger.log("Imagem detectada, iniciando download...")
                downloaded_image_path = await event.message.download_media()
                self.logger.log(f"Download concluído: {downloaded_image_path}")

            text_content = event.message.text or ""
            chat_title = getattr(event.chat, 'title', self.config.get('TELEGRAM_CANAL_MONITORADO', 'Desconhecido'))
            
            formatted_message = f"**Nova Mensagem**\n------------------------------------\n{text_content}" if text_content else f"`{chat_title}`"

            success = self.discord_service.send_message(formatted_message, image_path=downloaded_image_path)
            
            if success:
                self.logger.log("Mensagem encaminhada para o Discord com sucesso.")
            else:
                self.logger.log("[ERRO] Falha ao encaminhar para o Discord.")
        finally:
            if downloaded_image_path and os.path.exists(downloaded_image_path):
                self.logger.log(f"Limpando arquivo temporário: {downloaded_image_path}")
                os.remove(downloaded_image_path)

    def run(self):
        if not self.client:
            self.logger.log("[ERRO] O cliente não foi configurado. Encerrando.")
            return

        async def main():
 
            phone = self.config['TELEGRAM_PHONE_NUMBER']
            password = self.config.get('TELEGRAM_2FA_PASSWORD') or None

            await self.client.connect()
            if not await self.client.is_user_authorized():
                self.logger.log("Sessão não encontrada. Iniciando login...")
                await self.client.send_code_request(phone)
                self.logger.log("Um código de login foi enviado para o seu Telegram.")
                
                try:
                   
                    code = self.prompt_callback("Código de Login", "Por favor, insira o código recebido:")
                    if not code:
                        self.logger.log("[ERRO] Login cancelado. Código não inserido.")
                        return 
                    
                    await self.client.sign_in(phone, code)
                except SessionPasswordNeededError:
                    self.logger.log("Senha de 2 fatores (2FA) necessária.")
                    if not password:
                        
                        password = self.prompt_callback("Senha 2FA", "Sua senha de 2 fatores é necessária:")
                        if not password:
                            self.logger.log("[ERRO] Login cancelado. Senha não inserida.")
                            return
                    
                    await self.client.sign_in(password=password)
                
                self.logger.log("Login bem-sucedido!")
           

            channel = self.config['TELEGRAM_CANAL_MONITORADO']
            self.client.add_event_handler(self._message_handler, events.NewMessage(chats=[channel]))
            
            self.logger.log("Bot iniciado e escutando mensagens...")
            self.logger.log(f"Monitorando o canal: {channel}")
            self.logger.log("Ponte para o Discord está ATIVA.")
            
            await self.client.run_until_disconnected()

        try:
            self.loop.run_until_complete(main())
        except Exception as e:
            self.logger.log(f"[ERRO CRÍTICO] Ocorreu um erro no bot: {e}")
        finally:
            self.logger.log("Bot finalizado.")