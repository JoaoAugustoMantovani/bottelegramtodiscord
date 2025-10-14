import asyncio
from model import ConfigManager
from view import ConsoleView
from controller import TelegramController

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    

    view = ConsoleView()
    

    model = ConfigManager(view)
    

    app = TelegramController(model, view)
    
 
    try:
        app.run()
    except Exception as e:
        view.display_error(f"Uma exceção não tratada ocorreu: {e}")