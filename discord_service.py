import requests

class DiscordWebhookService:
    def __init__(self, webhook_url):
        if not webhook_url or not webhook_url.startswith("https://discord.com/api/webhooks/"):
            raise ValueError("URL de webhook do Discord inválida ou não fornecida.")
        
        # --- INÍCIO DA ALTERAÇÃO ---
        # Guarda a URL base sem quaisquer parâmetros
        self.base_webhook_url = webhook_url.split('?')[0]
        # A URL para enviar mensagens precisa do ?wait=true
        self.send_webhook_url = self.base_webhook_url + "?wait=true"
        # --- FIM DA ALTERAÇÃO ---

    def send_message(self, message_content, image_path=None):
        """
        Envia uma mensagem para a webhook.
        Retorna o ID da mensagem do Discord em caso de sucesso, None em caso de falha.
        """
        try:
            payload = {"content": message_content}
            
            # Usa a URL específica para envio
            if image_path is None:
                response = requests.post(self.send_webhook_url, json=payload)
            else:
                with open(image_path, 'rb') as f:
                    files = {'file1': (image_path, f)}
                    response = requests.post(self.send_webhook_url, data=payload, files=files)
            
            response.raise_for_status()
            return response.json().get('id')
        except requests.exceptions.RequestException as e:
            # Adiciona um registo mais detalhado
            self.log_error(f"Não foi possível enviar a mensagem", e)
            return None
        except FileNotFoundError:
            print(f"[ERRO DISCORD] Ficheiro de imagem não encontrado em: {image_path}")
            return None

    def edit_message(self, message_id, new_content):
        """
        Edita uma mensagem existente no Discord usando o seu ID.
        Retorna True se for bem-sucedido, False caso contrário.
        """
        try:
            # --- INÍCIO DA ALTERAÇÃO ---
            # Constrói a URL de edição a partir da URL base limpa
            edit_url = f"{self.base_webhook_url}/messages/{message_id}"
            # --- FIM DA ALTERAÇÃO ---
            
            payload = {"content": new_content}
            
            response = requests.patch(edit_url, json=payload)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            self.log_error(f"Não foi possível editar a mensagem {message_id}", e)
            return False
            
    # Função auxiliar para registar erros de forma consistente
    def log_error(self, message, error):
        print(f"[ERRO DISCORD] {message}: {error}")
        if error.response is not None:
            print(f"[ERRO DISCORD] Status Code: {error.response.status_code}")
            print(f"[ERRO DISCORD] Detalhes: {error.response.text}")