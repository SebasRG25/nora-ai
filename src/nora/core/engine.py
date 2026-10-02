import ollama
import re
from src.nora.core.persona import NoraPersona
from src.nora.memory.knowledge import NoraMemory

class NoraEngine:
    """
    Motor cognitivo local de N.O.R.A. usando Ollama con inyección de conocimientos.
    """
    def __init__(self, persona: NoraPersona):
        self.persona = persona
        self.memory = NoraMemory()
        self.model_name = "llama3.2" 
        
        self.conversation_history = []

    def process_input(self, user_text: str) -> str:
        # 1. Obtener todo lo que N.O.R.A sabe hasta ahora
        knowledge_text = self.memory.get_all_facts_text()
        
        # 2. Inyectar sus conocimientos en el prompt del sistema
        system_prompt = self.persona.get_system_prompt(knowledge_text)
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": user_text})
        
        try:
            # 3. Procesar localmente
            response = ollama.chat(
                model=self.model_name,
                messages=messages
            )
            
            ai_message = response['message']['content']
            
            # 4. Extraer nuevos aprendizajes (<LEARN>...</LEARN>)
            learn_matches = re.findall(r'<LEARN>(.*?)</LEARN>', ai_message, flags=re.IGNORECASE | re.DOTALL)
            for fact in learn_matches:
                self.memory.add_fact(fact.strip())
                
            # 5. Ocultar la etiqueta de la respuesta visible para el usuario
            clean_message = re.sub(r'<LEARN>.*?</LEARN>', '', ai_message, flags=re.IGNORECASE | re.DOTALL).strip()
            
            # Si su respuesta era SOLO la etiqueta, mostrar un mensaje de asimilación
            if not clean_message:
                clean_message = "*N.O.R.A. ha asimilado el conocimiento en silencio.*"
            
            # 6. Actualizar historial de corto plazo
            self.conversation_history.append({"role": "user", "content": user_text})
            self.conversation_history.append({"role": "assistant", "content": ai_message}) # Guardamos la versión con etiquetas para su propio contexto
            
            # Limitar historial para no saturar el contexto local
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return clean_message
            
        except Exception as e:
            return f"... (falla cognitiva local: {str(e)})"
