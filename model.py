import json
import os

class ConfigManager:
    """
    Gerencia o arquivo de configuração (config.json).
    Agora, apenas carrega e salva dados, sem interação com o usuário.
    """
    def __init__(self, config_file='config.json'):
        self.config_file = config_file

    def load_config(self):
        """Carrega a configuração do arquivo JSON. Se não existir, retorna um dict vazio."""
        if not os.path.exists(self.config_file):
            return {}
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception):
        
            return {}

    def save_config(self, config_data):
        """Salva o dicionário de configuração fornecido no arquivo JSON."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Erro ao salvar a configuração: {e}")
            return False