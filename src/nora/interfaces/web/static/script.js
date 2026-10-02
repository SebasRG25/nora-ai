const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// ----- CONFIGURACIÓN V-TUBER LIVE2D -----
const canvas = document.getElementById('live2d-canvas');
const app = new PIXI.Application({
    view: canvas,
    transparent: true,
    width: 300,
    height: 400
});

let noraModel;
// Usamos el modelo público 'Shizuku' que soporta emociones y seguimiento de ratón
const modelUrl = 'https://cdn.jsdelivr.net/gh/guansss/pixi-live2d-display/docs/assets/shizuku/shizuku.model.json';

PIXI.live2d.Live2DModel.from(modelUrl).then(model => {
    noraModel = model;
    app.stage.addChild(model);
    
    // Escalar y centrar el cuerpo 2D
    model.scale.set(0.18);
    model.x = 20;
    model.y = 30;

    // Hacer que los ojos y la cabeza sigan el cursor por toda la pantalla (Nos mira)
    document.addEventListener('mousemove', (e) => {
        // Mapeo simple de coordenadas
        model.focus(e.clientX, e.clientY);
    });
    
    // Reaccionar físicamente si le haces clic
    model.on('pointertap', () => {
        model.motion('tap_body');
    });
});

// Función para mapear las emociones elegidas por el LLM a expresiones faciales reales
function triggerFace(emotion) {
    if(!noraModel) return;
    
    // Expresiones de Shizuku: f01=neutral, f02=seria/pensando, f03=triste/confundida, f04=feliz
    if(emotion === 'happy') {
        noraModel.expression('f04');
        noraModel.motion('tap_body'); // Hace un pequeño baile
    } else if(emotion === 'confused' || emotion === 'curious') {
        noraModel.expression('f03');
    } else if(emotion === 'thinking') {
        noraModel.expression('f02');
    } else {
        noraModel.expression('f01'); // Neutral
    }
}
// ----------------------------------------

function addMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    msgDiv.innerHTML = `<strong>${sender === 'nora' ? 'N.O.R.A' : 'Tú'}:</strong> ${text}`;
    chatHistory.appendChild(msgDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;
    
    addMessage('user', text);
    userInput.value = '';
    sendBtn.disabled = true;
    
    triggerFace('thinking'); // Hace mueca de pensar mientras procesa localmente

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: text})
        });
        
        const data = await response.json();
        
        // Animamos su rostro según la emoción calculada por la IA
        triggerFace(data.face);
        
        // Volver a expresión neutral después de 4 segundos
        if(data.face !== 'neutral') {
            setTimeout(() => triggerFace('neutral'), 4000);
        }
        
        addMessage('nora', data.response);
        
    } catch (error) {
        addMessage('nora', 'Error cognitivo...');
        triggerFace('confused');
    } finally {
        sendBtn.disabled = false;
        userInput.focus();
    }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
