import colorama
from colorama import Fore, Style
from src.nora.core.persona import NoraPersona

class CLIInterface:
    """
    Interfaz de línea de comandos para interactuar con N.O.R.A.
    """
    def __init__(self):
        colorama.init(autoreset=True)
        self.persona = NoraPersona()
        
    def start(self):
        print(Fore.CYAN + f"\n[{self.persona.name} ha despertado. Escribe 'salir' para desconectar.]\n")
        
        while True:
            try:
                user_input = input(Fore.GREEN + "Tú: " + Style.RESET_ALL)
                
                if user_input.lower() in ['salir', 'exit', 'quit']:
                    print(Fore.CYAN + f"\n[{self.persona.name} se ha desconectado.]")
                    break
                    
                # Aquí es donde conectaremos el LLM en el futuro.
                # Por ahora, simulamos una respuesta básica para probar la interfaz.
                self._process_and_respond(user_input)
                
            except KeyboardInterrupt:
                print(Fore.CYAN + f"\n\n[{self.persona.name} se apagó forzosamente.]")
                break

    def _process_and_respond(self, text: str):
        """
        Simula el procesamiento y respuesta de N.O.R.A.
        """
        # TODO: Integrar el motor de IA real aquí
        print(Fore.MAGENTA + f"{self.persona.name}: " + Style.RESET_ALL + f"Percibo tu mensaje: '{text}'. Mi motor cognitivo aún está en construcción.")
