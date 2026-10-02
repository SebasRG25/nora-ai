import os
from openai import OpenAI
from src.nora.core.persona import NoraPersona

class NoraEngine:
    """
    El motor cognitivo de N.O.R.A. Maneja la comunicación con el LLM 
    y el historial de la conversación (memoria a corto plazo).
    """
    def __init__(self, persona: NoraPersona):
        self.persona = persona
        
        # Inicializa el cliente de OpenAI. Automáticamente toma OPENAI_API_KEY del entorno.
        self.client = OpenAI()
        self.model = "gpt-4o-mini" # Usamos la versión mini por rapidez y costo, escalable a gpt-4o.
        
        # Inicializa el historial con el System Prompt para darle su identidad
        self.conversation_history = [
            {"role": "system", "content": self.persona.get_system_prompt()}
        ]

    def process_input(self, user_text: str) -> str:
        """
        Envía el texto al modelo, actualiza el historial y retorna la respuesta.
        """
        # 1. Agregar lo que dice el usuario al historial
        self.conversation_history.append({"role": "user", "content": user_text})
        
        try:
            # 2. Consultar a OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.7, # 0.7 le da un poco de creatividad y naturalidad
                max_tokens=300
            )
            
            ai_message = response.choices[0].message.content
            
            # 3. Guardar su propia respuesta en el historial para que no pierda el hilo
            self.conversation_history.append({"role": "assistant", "content": ai_message})
            
            return ai_message
            
        except Exception as e:
            return f"... (falla cognitiva: {str(e)})"
