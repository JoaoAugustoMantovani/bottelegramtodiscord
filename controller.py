import os
import asyncio
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from discord_service import DiscordWebhookService
from message_store import MessageStore

class TelegramController:
    def __init__(self, config, logger, prompt_callback):
        self.config = config
        self.logger = logger
        self.prompt_callback = prompt_callback 
        self.discord_service = None
        self.client = None
        self.loop = None
        self.message_store = MessageStore(expiry_days=14)

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
        self.logger.log(f"--- NOVO EVENTO: NewMessage ---")
        self.logger.log(f"[DEBUG] ID da mensagem recebida no Telegram: {event.message.id}")

        downloaded_image_path = None
        try:
            if event.message.photo:
                self.logger.log("[DEBUG] Imagem detetada, a iniciar o download...")
                downloaded_image_path = await event.message.download_media()

            text_content = event.message.text or ""
            chat_title = getattr(event.chat, 'title', event.chat_id)
            formatted_message = f"**Nova Mensagem de `{chat_title}`**\n------------------------------------\n{text_content}" if text_content else f"**Nova Imagem de `{chat_title}`**"

            discord_message_id = self.discord_service.send_message(formatted_message, image_path=downloaded_image_path)

            if discord_message_id:
                self.logger.log(f"[DEBUG] Mensagem encaminhada para o Discord. ID do Discord: {discord_message_id}")
                self.message_store.add_mapping(event.message.id, discord_message_id)
                self.logger.log(f"[DEBUG] Mapeamento adicionado: Telegram ID {event.message.id} -> Discord ID {discord_message_id}")
            else:
                self.logger.log("[ERRO] Falha ao encaminhar a mensagem para o Discord (send_message retornou None).")
        finally:
            if downloaded_image_path and os.path.exists(downloaded_image_path):
                os.remove(downloaded_image_path)
        self.logger.log(f"--- FIM DO EVENTO: NewMessage ---")


    async def _message_edited_handler(self, event):
        self.logger.log(f"--- NOVO EVENTO: MessageEdited ---")
        telegram_message_id = event.message.id
        self.logger.log(f"[DEBUG] O Telegram reportou uma edição para a mensagem ID: {telegram_message_id}")

        self.logger.log(f"[DEBUG] A tentar encontrar o mapeamento. Mapa atual: {self.message_store.message_map}")
        discord_message_id = self.message_store.get_mapping(telegram_message_id)

        if not discord_message_id:
            self.logger.log(f"[AVISO] Mapeamento não encontrado para a mensagem editada (ID Telegram: {telegram_message_id}). A ignorar.")
            self.logger.log(f"--- FIM DO EVENTO: MessageEdited ---")
            return

        self.logger.log(f"[DEBUG] Mapeamento encontrado! ID do Discord correspondente: {discord_message_id}")
        chat_title = getattr(event.chat, 'title', event.chat_id)
        new_text_content = event.message.text or ""
        formatted_message = f"**Nova Mensagem de `{chat_title}`** `(editado)`\n------------------------------------\n{new_text_content}"

        success = self.discord_service.edit_message(discord_message_id, formatted_message)

        if success:
            self.logger.log(f"[DEBUG] Mensagem (ID Discord: {discord_message_id}) atualizada com sucesso.")
        else:
            self.logger.log(f"[ERRO] Falha ao atualizar a mensagem (ID Discord: {discord_message_id}) no Discord.")
        self.logger.log(f"--- FIM DO EVENTO: MessageEdited ---")

    def run(self):
        if not self.client:
            self.logger.log("[ERRO] O cliente não foi configurado. A encerrar.")
            return

        async def main():
            self.logger.log("A verificar mapeamentos de mensagens expirados...")
            cleaned_count = self.message_store.cleanup_expired_entries()
            if cleaned_count > 0:
                self.logger.log(f"{cleaned_count} mapeamentos antigos foram removidos com sucesso.")

            phone = self.config['TELEGRAM_PHONE_NUMBER']
            password = self.config.get('TELEGRAM_2FA_PASSWORD') or None
            await self.client.connect()
            if not await self.client.is_user_authorized():
                self.logger.log("Sessão não encontrada. A iniciar login...")
                await self.client.send_code_request(phone)
                try:
                    code = self.prompt_callback("Código de Login", "Insira o código:")
                    if not code:
                        self.logger.log("[ERRO] Login cancelado.")
                        return
                    await self.client.sign_in(phone, code)
                except SessionPasswordNeededError:
                    if not password:
                        password = self.prompt_callback("Senha 2FA", "Insira a senha:")
                    if not password:
                        self.logger.log("[ERRO] Login cancelado.")
                        return
                    await self.client.sign_in(password=password)
                self.logger.log("Login bem-sucedido!")

            channels_list = self.config.get("TELEGRAM_CANAIS_MONITORADOS", [])
            if not channels_list:
                self.logger.log("[ERRO] Nenhum canal configurado. A encerrar.")
                return

            entities = [int(c) if c.strip().lstrip('-').isdigit() else c.strip() for c in channels_list]

            self.client.add_event_handler(self._message_handler, events.NewMessage(chats=entities))
            self.logger.log("[DEBUG] Handler para NewMessage registado.")
            self.client.add_event_handler(self._message_edited_handler, events.MessageEdited(chats=entities))
            self.logger.log("[DEBUG] Handler para MessageEdited registado.")

            self.logger.log("Bot iniciado e a escutar novas mensagens e edições...")
            self.logger.log(f"A monitorizar {len(entities)} canais.")
            self.logger.log("Ponte para o Discord está ATIVA.")

            await self.client.run_until_disconnected()

        try:
            self.loop.run_until_complete(main())
        except Exception as e:
            self.logger.log(f"[ERRO CRÍTICO] Ocorreu um erro no bot: {e}")
        finally:
            self.logger.log("Bot finalizado.")