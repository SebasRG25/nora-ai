import os
import google.generativeai as genai
from src.nora.core.persona import NoraPersona

class NoraEngine:
    """
    El motor cognitivo de N.O.R.A. Maneja la comunicación con el LLM de Google (Gemini)
    y el historial de la conversación (memoria a corto plazo).
    """
    def __init__(self, persona: NoraPersona):
        self.persona = persona
        
        # Configurar la API de Google con la clave del entorno
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Inicializamos el modelo (gemini-1.5-flash es muy rápido, pero si tienes pro puedes usar gemini-1.5-pro)
        # Le inyectamos directamente su identidad a través de las instrucciones del sistema
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=self.persona.get_system_prompt()
        )
        
        # start_chat maneja automáticamente el historial (memoria a corto plazo) por nosotros
        self.chat_session = self.model.start_chat(history=[])

    def process_input(self, user_text: str) -> str:
        """
        Envía el texto al modelo, el cual ya mantiene el contexto, y retorna la respuesta.
        """
        try:
            # Enviar mensaje a Gemini
            response = self.chat_session.send_message(user_text)
            return response.text
            
        except Exception as e:
            return f"... (falla cognitiva en la red Gemini: {str(e)})"
