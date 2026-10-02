import ollama
from src.nora.core.persona import NoraPersona

class NoraEngine:
    """
    Motor cognitivo de N.O.R.A. usando Ollama (100% Local y Privado).
    """
    def __init__(self, persona: NoraPersona):
        self.persona = persona
        # Usamos el modelo que acabas de descargar
        self.model_name = "llama3.2" 
        
        # Historial de conversación (Memoria a Corto Plazo)
        self.conversation_history = []

    def process_input(self, user_text: str) -> str:
        """
        Aprende, actualiza el prompt de su "edad" y consulta a Ollama localmente.
        """
        # 1. Envejecer/Aprender un poco con cada interacción
        self.persona.learn()
        
        # 2. Reconstruir su identidad dinámica según la fase en la que esté
        messages = [{"role": "system", "content": self.persona.get_system_prompt()}]
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": user_text})
        
        try:
            # 3. Llamar a Ollama localmente (sin internet)
            response = ollama.chat(
                model=self.model_name,
                messages=messages
            )
            
            ai_message = response['message']['content']
            
            # 4. Guardar en la memoria de esta sesión
            self.conversation_history.append({"role": "user", "content": user_text})
            self.conversation_history.append({"role": "assistant", "content": ai_message})
            
            return ai_message
            
        except Exception as e:
            return f"... (falla cognitiva local: asegúrate de que Ollama esté corriendo en segundo plano. Error: {str(e)})"
