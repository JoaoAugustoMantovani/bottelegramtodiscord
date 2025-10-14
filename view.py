from datetime import datetime

class ConsoleView:
    """
    Responsável por toda a saída de dados para o console.
    """
    def display_message(self, message):
        """Formata e exibe uma mensagem recebida do Telegram."""
        chat_title = message.chat.title if hasattr(message.chat, 'title') else f"Chat ID {message.chat.id}"
        sender_name = message.sender.first_name if hasattr(message.sender, 'first_name') and message.sender.first_name else "Desconhecido"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print("-" * 50)
        print(f"[{timestamp}] Nova mensagem!")
        print(f"  Canal/Grupo: {chat_title} ({message.chat.id})")
        print(f"  De: {sender_name}")
        print(f"  Mensagem: {message.text}")
        print("-" * 50 + "\n")

    def display_info(self, text):
        """Exibe uma mensagem informativa."""
        print(f"[INFO] {text}")

    def display_error(self, text):
        """Exibe uma mensagem de erro."""
        print(f"[ERRO] {text}")
        
    def display_success(self, text):
        """Exibe uma mensagem de sucesso."""
        print(f"[SUCESSO] {text}")

    def get_user_input(self, prompt):
        """Obtém uma entrada do usuário."""
        return input(prompt)