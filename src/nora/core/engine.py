import os
from google import genai
from google.genai import types
from src.nora.core.persona import NoraPersona

class NoraEngine:
    """
    El motor cognitivo de N.O.R.A. Maneja la comunicación con el LLM de Google (Gemini)
    y el historial de la conversación usando el nuevo SDK google-genai.
    """
    def __init__(self, persona: NoraPersona):
        self.persona = persona
        
        # Cliente del nuevo SDK oficial de Google (google-genai)
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        self.model_name = "gemini-3.5-flash"
        
        # Configuramos la identidad a través de las instrucciones del sistema
        config = types.GenerateContentConfig(
            system_instruction=self.persona.get_system_prompt(),
            temperature=0.7
        )
        
        # Iniciamos el chat que maneja la memoria a corto plazo
        self.chat_session = self.client.chats.create(
            model=self.model_name,
            config=config
        )

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
