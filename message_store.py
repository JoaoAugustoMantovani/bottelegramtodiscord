import json
import os
import time
from datetime import timedelta

class MessageStore:
    """
    Gerencia o armazenamento persistente do mapa de mensagens em um arquivo JSON.
    Inclui a lógica para limpar entradas expiradas.
    """
    def __init__(self, store_file='message_map.json', expiry_days=14):
        self.store_file = store_file
        self.expiry_duration = timedelta(days=expiry_days).total_seconds()
        self.message_map = self._load_map()

    def _load_map(self):
        """Carrega o mapa do arquivo JSON. Se não existir, retorna um dict vazio."""
        if not os.path.exists(self.store_file):
            return {}
        try:
            with open(self.store_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception):
           
            return {}

    def _save_map(self):
        """Salva o mapa atual no arquivo JSON."""
        try:
            with open(self.store_file, 'w', encoding='utf-8') as f:
                json.dump(self.message_map, f, indent=4)
        except Exception as e:
            print(f"[ERRO DE ARMAZENAMENTO] Não foi possível salvar o mapa de mensagens: {e}")

    def add_mapping(self, telegram_id, discord_id):
        """Adiciona um novo mapeamento com um timestamp."""
       
        self.message_map[str(telegram_id)] = {
            "discord_id": discord_id,
            "timestamp": time.time()
        }
        self._save_map()

    def get_mapping(self, telegram_id):
        """Obtém o ID do Discord para um ID do Telegram."""
        entry = self.message_map.get(str(telegram_id))
        return entry["discord_id"] if entry else None

    def cleanup_expired_entries(self):
        """
        Verifica o mapa e remove todas as entradas mais antigas que a duração de expiração.
        Retorna o número de entradas removidas.
        """
        current_time = time.time()
        expired_keys = [
            key for key, value in self.message_map.items()
            if current_time - value.get("timestamp", 0) > self.expiry_duration
        ]
        
        for key in expired_keys:
            del self.message_map[key]
            
        if expired_keys:
            self._save_map()
            
        return len(expired_keys)