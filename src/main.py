import os
import sys
from dotenv import load_dotenv

# Asegurar que el path incluya src para importar nora
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.nora.interfaces.web.app import start_web

def main():
    # Cargar variables de entorno
    load_dotenv()
    
    # Arrancar el servidor web
    start_web()

if __name__ == "__main__":
    main()
