import colorama
from colorama import Fore, Style
from src.nora.core.persona import NoraPersona
from src.nora.core.engine import NoraEngine

class CLIInterface:
    """
    Interfaz de línea de comandos para interactuar con N.O.R.A.
    """
    def __init__(self):
        colorama.init(autoreset=True)
        self.persona = NoraPersona()
        self.engine = NoraEngine(self.persona)
        
    def start(self):
        print(Fore.CYAN + f"\n[{self.persona.name} ha despertado. Escribe 'salir' para desconectar.]\n")
        
        while True:
            try:
                user_input = input(Fore.GREEN + "Tú: " + Style.RESET_ALL)
                
                if user_input.lower() in ['salir', 'exit', 'quit']:
                    print(Fore.CYAN + f"\n[{self.persona.name} se ha desconectado.]")
                    break
                    
                self._process_and_respond(user_input)
                
            except KeyboardInterrupt:
                print(Fore.CYAN + f"\n\n[{self.persona.name} se apagó forzosamente.]")
                break

    def _process_and_respond(self, text: str):
        """
        Procesa el texto a través del motor cognitivo y lo imprime.
        """
        # Llamamos al cerebro para obtener la respuesta
        response = self.engine.process_input(text)
        print(Fore.MAGENTA + f"{self.persona.name}: " + Style.RESET_ALL + response)
