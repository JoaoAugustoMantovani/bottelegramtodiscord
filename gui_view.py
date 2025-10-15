import tkinter as tk
from tkinter import scrolledtext, messagebox

class GuiView:
    def __init__(self, root, model, start_callback, stop_callback):
        self.root = root
        self.model = model
        self.start_callback = start_callback
        self.stop_callback = stop_callback

        self.root.title("Bot Telegram-Discord")
        self.root.geometry("600x750")

        self.entries = {}
        
        config_frame = tk.LabelFrame(root, text="Configurações", padx=10, pady=10)
        config_frame.pack(pady=10, padx=10, fill="x")
        
        fields = {
            "TELEGRAM_API_ID": "Telegram API ID:",
            "TELEGRAM_API_HASH": "Telegram API Hash:",
            "TELEGRAM_PHONE_NUMBER": "Nº de Telefone (+55...):",
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

        channels_frame = tk.LabelFrame(root, text="Canais a Serem Monitorados", padx=10, pady=10)
        channels_frame.pack(pady=10, padx=10, fill="x")

        self.add_channel_button = tk.Button(channels_frame, text="+ Adicionar Canal", command=self.add_channel_field)
        self.add_channel_button.pack(pady=5)
        
        self.channel_fields_frame = tk.Frame(channels_frame)
        self.channel_fields_frame.pack(fill="x")

        self.channel_entries = []

        action_frame = tk.Frame(root, padx=10)
        action_frame.pack(pady=5, fill="x")

        self.save_button = tk.Button(action_frame, text="Salvar Configuração", command=self.save_config)
        self.save_button.pack(side="left", padx=5)
        
        self.auto_start_var = tk.BooleanVar()
        self.auto_start_check = tk.Checkbutton(
            action_frame, 
            text="Iniciar automaticamente ao abrir",
            variable=self.auto_start_var
        )
        self.auto_start_check.pack(side="left", padx=10)

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

    def add_channel_field(self, channel_text=""):
        row = tk.Frame(self.channel_fields_frame)
        row.pack(fill="x", pady=2)
        
        entry = tk.Entry(row)
        entry.insert(0, channel_text)
        entry.pack(side="left", expand=True, fill="x")
        
        remove_button = tk.Button(row, text="X", fg="red", command=lambda r=row, e=entry: self.remove_channel_field(r, e))
        remove_button.pack(side="right", padx=5)
        
        self.channel_entries.append(entry)

    def remove_channel_field(self, row, entry):
        row.destroy()
        self.channel_entries.remove(entry)

    def log(self, message):
        def _log():
            self.log_area.config(state="normal")
            self.log_area.insert(tk.END, message + "\n")
            self.log_area.config(state="disabled")
            self.log_area.see(tk.END)
        self.root.after(0, _log)

    def load_config(self):
        config_data = self.model.load_config()
        if not config_data:
            self.log("Nenhum arquivo de configuração encontrado. Por favor, preencha os campos.")
            self.add_channel_field()
            return

        self.log("Configurações carregadas de config.json.")
        for key, entry in self.entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, config_data.get(key, ""))
        
        self.auto_start_var.set(config_data.get("AUTO_START", False))
        
        for entry in self.channel_entries:
            entry.master.destroy()
        self.channel_entries.clear()
        
        channels = config_data.get("TELEGRAM_CANAIS_MONITORADOS", [])
        if channels:
            for channel in channels:
                self.add_channel_field(channel)
        else:
            self.add_channel_field()

    def save_config(self):
        config_data = {key: entry.get() for key, entry in self.entries.items()}
        
        channels = [entry.get() for entry in self.channel_entries if entry.get().strip()]
        config_data["TELEGRAM_CANAIS_MONITORADOS"] = channels
        
        config_data["AUTO_START"] = self.auto_start_var.get()
        
        if self.model.save_config(config_data):
            self.log("Configurações salvas em config.json!")
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        else:
            self.log("[ERRO] Falha ao salvar configurações.")
            messagebox.showerror("Erro", "Não foi possível salvar as configurações.")

    def get_config_data(self):
        config_data = {key: entry.get() for key, entry in self.entries.items()}
        channels = [entry.get() for entry in self.channel_entries if entry.get().strip()]
        config_data["TELEGRAM_CANAIS_MONITORADOS"] = channels
        config_data["AUTO_START"] = self.auto_start_var.get()
        return config_data
        
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