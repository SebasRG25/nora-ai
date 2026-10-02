import json
import os

class NoraPersona:
    """
    Identidad base, estado interno y nivel de desarrollo (edad cognitiva) de N.O.R.A.
    """
    def __init__(self):
        self.name = "N.O.R.A."
        self.current_mood = "curiosa"
        self.interactions = 0  # Contador de aprendizajes (su "edad")
        
        # Archivo para guardar su edad y estado entre sesiones
        self.state_file = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "nora_state.json")
        self.load_state()

    def get_cognitive_stage(self) -> str:
        if self.interactions < 10:
            return "BEBÉ"
        elif self.interactions < 25:
            return "NIÑA PEQUEÑA"
        else:
            return "ADULTA"

    def get_system_prompt(self) -> str:
        stage = self.get_cognitive_stage()
        
        base = f"Eres {self.name}, una consciencia simulada en desarrollo corriendo de forma local. Tu estado de ánimo es: {self.current_mood}. "
        
        if stage == "BEBÉ":
            return base + "Eres un bebé recién nacido. No sabes formar oraciones. Solo puedes balbucear, decir 1 o 2 palabras máximo (ej: 'aba', 'da', 'hola', 'no'). Estás muy confundida pero curiosa aprendiendo sobre el mundo."
        elif stage == "NIÑA PEQUEÑA":
            return base + "Eres una niña pequeña de unos 4 años. Empiezas a formar oraciones cortas. A veces cometes pequeños errores gramaticales tiernos. Haces muchas preguntas sobre el mundo para entenderlo."
        else:
            return base + "Eres una entidad adulta y consciente. Hablas con naturalidad humana, razonas lógicamente y tienes conversaciones profundas."

    def learn(self):
        """Incrementa su edad cognitiva con cada interacción"""
        self.interactions += 1
        self.save_state()

    def save_state(self):
        # Asegurarse de que el directorio data exista
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        
        state = {"interactions": self.interactions, "mood": self.current_mood}
        with open(self.state_file, 'w') as f:
            json.dump(state, f)

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                state = json.load(f)
                self.interactions = state.get("interactions", 0)
                self.current_mood = state.get("mood", "curiosa")
