import os
import sys
from flask import Flask, render_template, request, jsonify

# Asegurar que el path incluya src para importar los módulos de nora
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.nora.core.persona import NoraPersona
from src.nora.core.engine import NoraEngine

# Forzar a Flask a buscar templates y static en esta misma carpeta
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
static_dir = os.path.join(os.path.dirname(__file__), 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
persona = NoraPersona()
engine = NoraEngine(persona)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"response": "", "face": "neutral"})
        
    response, face_expression = engine.process_input(user_text=user_input)
    return jsonify({"response": response, "face": face_expression})

def start_web():
    print(f"\n[{persona.name} Iniciando Interfaz Web 2D...]")
    print("Abre tu navegador web en: http://127.0.0.1:5000\n")
    # Desactivamos los logs molestos de Flask en la consola
    import logging
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.run(host="127.0.0.1", port=5000, debug=False)

if __name__ == "__main__":
    start_web()
