import tkinter as tk
from tkinter import scrolledtext, messagebox

class GuiView:
    def __init__(self, root, model, start_callback, stop_callback):
        self.root = root
        self.model = model
        self.start_callback = start_callback
        self.stop_callback = stop_callback

        self.root.title("Bot Telegram-Discord")
        self.root.geometry("600x680") 

        self.entries = {}
        
        config_frame = tk.LabelFrame(root, text="Configurações", padx=10, pady=10)
        config_frame.pack(pady=10, padx=10, fill="x")
        
        fields = {
            "TELEGRAM_API_ID": "Telegram API ID:",
            "TELEGRAM_API_HASH": "Telegram API Hash:",
            "TELEGRAM_PHONE_NUMBER": "Nº de Telefone (+55...):",
            "TELEGRAM_CANAL_MONITORADO": "Canal para Monitorar (@...):",
            "DISCORD_WEBHOOK_URL": "URL Webhook Discord:",
           
            "TELEGRAM_2FA_PASSWORD": "Senha 2 Fatores (se houver):"
        }
        
        for key, text in fields.items():
            row = tk.Frame(config_frame)
            row.pack(fill="x", pady=2)
            label = tk.Label(row, width=25, text=text, anchor='w')
            entry = tk.Entry(row)
           
            if "PASSWORD" in key:
                entry.config(show="*")
            label.pack(side="left")
            entry.pack(side="right", expand=True, fill="x")
            self.entries[key] = entry
            
        action_frame = tk.Frame(root, padx=10)
        action_frame.pack(pady=5, fill="x")

        self.save_button = tk.Button(action_frame, text="Salvar Configuração", command=self.save_config)
        self.save_button.pack(side="left", padx=5)

        self.start_button = tk.Button(action_frame, text="▶ Iniciar Bot", command=self.start_bot, bg="green", fg="white")
        self.start_button.pack(side="right", padx=5)

        self.stop_button = tk.Button(action_frame, text="■ Parar Bot", command=self.stop_bot, bg="red", fg="white", state="disabled")
        self.stop_button.pack(side="right", padx=5)

        log_frame = tk.LabelFrame(root, text="Logs", padx=10, pady=10)
        log_frame.pack(pady=10, padx=10, expand=True, fill="both")

        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state="disabled")
        self.log_area.pack(expand=True, fill="both")

        self.load_config()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def log(self, message):
        def _log():
            self.log_area.config(state="normal")
            self.log_area.insert(tk.END, message + "\n")
            self.log_area.config(state="disabled")
            self.log_area.see(tk.END)
        self.root.after(0, _log)

    def load_config(self):
        config_data = self.model.load_config()
        if config_data:
            self.log("Configurações carregadas de config.json.")
            for key, entry in self.entries.items():
                entry.delete(0, tk.END) 
                entry.insert(0, config_data.get(key, ""))
        else:
            self.log("Nenhum arquivo de configuração encontrado. Por favor, preencha os campos.")

    def save_config(self):
        config_data = {key: entry.get() for key, entry in self.entries.items()}
        if self.model.save_config(config_data):
            self.log("Configurações salvas em config.json!")
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        else:
            self.log("[ERRO] Falha ao salvar configurações.")
            messagebox.showerror("Erro", "Não foi possível salvar as configurações.")

    def get_config_data(self):
        return {key: entry.get() for key, entry in self.entries.items()}

    def start_bot(self):
        self.start_button.config(state="disabled")
        self.save_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.start_callback()

    def stop_bot(self):
        self.log("Solicitando parada do bot...")
        self.stop_callback()

    def on_bot_stopped(self):
        def _update_ui():
            self.start_button.config(state="normal")
            self.save_button.config(state="normal")
            self.stop_button.config(state="disabled")
        self.root.after(0, _update_ui)

    def on_closing(self):
        if messagebox.askokcancel("Sair", "Deseja fechar o bot?"):
            self.stop_callback()
            self.root.destroy()