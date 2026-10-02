import json
import os
import re

class NoraMemory:
    """
    Gestiona la base de conocimientos explícitos de N.O.R.A. (Memoria a Largo Plazo).
    Todo lo que aprende se guarda aquí.
    """
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "knowledge.json")
        self.facts = []
        self.load()
        
    def load(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as f:
                self.facts = json.load(f)
                
    def save(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.facts, f, ensure_ascii=False, indent=2)
            
    def add_fact(self, fact: str):
        if fact not in self.facts:
            self.facts.append(fact)
            self.save()
            
    def get_all_facts_text(self) -> str:
        if not self.facts:
            return ""
        return "\n".join([f"- {fact}" for fact in self.facts])
