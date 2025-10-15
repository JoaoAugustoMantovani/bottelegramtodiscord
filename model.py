import json
import os

class ConfigManager:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file

    def load_config(self):
        if not os.path.exists(self.config_file):
            return {}
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
               
                if "TELEGRAM_CANAL_MONITORADO" in config:
                    old_channel = config["TELEGRAM_CANAL_MONITORADO"]
                    if old_channel:
                        config["TELEGRAM_CANAIS_MONITORADOS"] = [old_channel]
                    del config["TELEGRAM_CANAL_MONITORADO"]
                return config
        except (json.JSONDecodeError, Exception):
            return {}

    def save_config(self, config_data):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Erro ao salvar a configuração: {e}")
            return False