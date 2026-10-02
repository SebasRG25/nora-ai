const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// ----- 1. GARANTIZAR QUE EL CHAT FUNCIONE PRIMERO -----
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
    
    triggerFace('thinking'); // Cara de pensar mientras carga

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: text})
        });
        
        const data = await response.json();
        
        // Poner la animación que NORA eligió
        triggerFace(data.face);
        
        if(data.face !== 'neutral') {
            setTimeout(() => triggerFace('neutral'), 4000);
        }
        
        addMessage('nora', data.response);
        
    } catch (error) {
        addMessage('nora', 'Error de conexión cognitiva.');
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

// ----- 2. CARGAR AVATAR DE FORMA SEGURA (SIN ROMPER EL CHAT) -----
let noraModel = null;

function triggerFace(emotion) {
    if(!noraModel) return;
    try {
        // En un modelo Cubism 4 (como Hiyori), las expresiones pueden llamarse distinto.
        // Forzaremos movimientos seguros que todos los modelos tienen
        noraModel.motion('TapBody'); 
    } catch(e) {}
}

try {
    const canvas = document.getElementById('live2d-canvas');
    if (window.PIXI && window.PIXI.live2d) {
        const app = new PIXI.Application({
            view: canvas,
            transparent: true,
            width: 300,
            height: 400
        });

        // Usamos a 'Hiyori', un modelo moderno (Cubism 4) oficial súper estable
        const modelUrl = 'https://cdn.jsdelivr.net/gh/guansss/pixi-live2d-display/docs/assets/hiyori/hiyori_pro_t10.model3.json';

        PIXI.live2d.Live2DModel.from(modelUrl).then(model => {
            noraModel = model;
            app.stage.addChild(model);
            
            // Escalar y centrar
            model.scale.set(0.12);
            model.x = 20;
            model.y = 50;

            // Seguir el ratón
            document.addEventListener('mousemove', (e) => {
                model.focus(e.clientX, e.clientY);
            });
            
            model.on('pointertap', () => {
                model.motion('TapBody');
            });
        }).catch(err => {
            console.warn("No se pudo cargar el avatar, pero el chat seguirá funcionando.", err);
        });
    }
} catch (error) {
    console.warn("Fallo al iniciar el motor 2D:", error);
}
