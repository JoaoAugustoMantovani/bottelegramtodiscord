import requests

class DiscordWebhookService:
    """
    Serviço responsável por enviar mensagens, com ou sem imagens, para uma webhook do Discord.
    """
    def __init__(self, webhook_url):
        if not webhook_url or not webhook_url.startswith("https://discord.com/api/webhooks/"):
            raise ValueError("URL de webhook do Discord inválida ou não fornecida.")
        self.webhook_url = webhook_url

    def send_message(self, message_content, image_path=None):
        """
        Envia uma mensagem para a webhook.
        Se 'image_path' for fornecido, anexa a imagem à mensagem.
        Retorna True se for bem-sucedido, False caso contrário.
        """
        try:
          
            payload = { "content": message_content }
            
            if image_path is None:
              
                response = requests.post(self.webhook_url, json=payload)
            else:
              
                with open(image_path, 'rb') as f:
                  
                    files = {'file1': (image_path, f)}
                    
                    response = requests.post(self.webhook_url, data=payload, files=files)
            
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"[ERRO DISCORD] Não foi possível enviar a mensagem: {e}")
         
            if e.response is not None:
                print(f"[ERRO DISCORD] Detalhes: {e.response.text}")
            return False
        except FileNotFoundError:
            print(f"[ERRO DISCORD] Arquivo de imagem não encontrado em: {image_path}")
            return False