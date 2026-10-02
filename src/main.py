import os
import sys
from dotenv import load_dotenv

# Asegurar que el path incluya src para importar nora
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.nora.interfaces.cli import CLIInterface

def main():
    # Cargar variables de entorno
    load_dotenv()
    
    # Inicializar la interfaz CLI
    print("Iniciando la secuencia de arranque de N.O.R.A...")
    cli = CLIInterface()
    cli.start()

if __name__ == "__main__":
    main()
