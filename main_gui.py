import sys
import tkinter as tk
from tkinter import simpledialog
import threading
import os
from PIL import Image
import pystray

from gui_view import GuiView
from model import ConfigManager
from controller import TelegramController

def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, funcionando tanto no modo de desenvolvimento quanto no PyInstaller. """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.bot_thread = None
        self.controller = None
        self.tray_icon = None

        self.model = ConfigManager()
        self.view = GuiView(root, self.model, self.start_bot_thread, self.stop_bot_thread)
        
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        
        tray_icon_successful = self.setup_tray_icon()
        if not tray_icon_successful:
            self.show_window()
        else:
            self.hide_window()

    def setup_tray_icon(self):
      
        try:
            image = Image.open(resource_path("icon.png"))
            menu = (
                pystray.MenuItem("Mostrar", self.show_window, default=True),
                pystray.MenuItem("Sair", self.exit_application)
            )
            self.tray_icon = pystray.Icon("BotTelegramDiscord", image, "Bot Telegram-Discord", menu)
            tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            tray_thread.start()
            return True 
        except FileNotFoundError:
            self.view.log("[ERRO FATAL] Arquivo 'icon.png' não encontrado na pasta!")
            self.view.log("O ícone da bandeja não pôde ser criado.")
            return False 
        except Exception as e:
            self.view.log(f"[ERRO FATAL] Falha ao criar ícone da bandeja: {e}")
            self.view.log("Verifique se o arquivo 'icon.png' é uma imagem válida.")
            return False 

    def hide_window(self):
      
        if self.tray_icon and self.tray_icon.visible:
            self.root.withdraw()
            self.view.log("Aplicação minimizada para a bandeja do sistema.")
        else:
            self.view.log("Ícone da bandeja não está ativo. A janela não será escondida.")

    def show_window(self):
    
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def exit_application(self):
       
        self.view.log("Encerrando a aplicação...")
        if self.bot_thread and self.bot_thread.is_alive():
            self.stop_bot_thread()
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()
        self.root.destroy()
   
    def prompt_for_input(self, title, prompt):
       
        result_holder = []
        event = threading.Event()
        def _ask_string():
            try:
                result = simpledialog.askstring(title, prompt, parent=self.root)
                result_holder.append(result)
            finally:
                event.set()
        self.root.after(0, _ask_string)
        event.wait()
        return result_holder[0] if result_holder else None
        
    def start_bot_thread(self):
        config_data = self.view.get_config_data()
        
       
        required_fields = ["TELEGRAM_API_ID", "TELEGRAM_API_HASH", "TELEGRAM_PHONE_NUMBER", "DISCORD_WEBHOOK_URL"]
        
       
        if not all(config_data.get(k) for k in required_fields):
            self.view.log("[ERRO] Todos os campos (exceto senha) devem ser preenchidos!")
            self.view.on_bot_stopped()
            return
        
      
        if not config_data.get("TELEGRAM_CANAIS_MONITORADOS"):
            self.view.log("[ERRO] Adicione pelo menos um canal para monitorar!")
            self.view.on_bot_stopped()
            return
      

        self.controller = TelegramController(config_data, self.view, self.prompt_for_input)
        def run_in_thread():
            if self.controller.setup():
                self.controller.run()
            self.root.after(0, self.view.on_bot_stopped)
        self.bot_thread = threading.Thread(target=run_in_thread, daemon=True)
        self.bot_thread.start()

    def stop_bot_thread(self):
      
        if self.controller and self.controller.client:
            self.view.log("Desconectando o cliente Telegram...")
            if self.controller.loop and self.controller.client.is_connected():
                self.controller.loop.call_soon_threadsafe(self.controller.client.disconnect)
        else:
            self.view.log("Bot não estava rodando ou já foi parado.")
            self.view.on_bot_stopped()

if __name__ == "__main__":
    
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()