const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

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
    
    triggerFace('thinking'); 

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: text})
        });
        
        const data = await response.json();
        
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

if(sendBtn) sendBtn.addEventListener('click', sendMessage);
if(userInput) userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});


// ----- CARGA DEL AVATAR (CON FALLBACK A SVG SI FALLA EL 3D) -----
let noraModel = null;
const avatarWrapper = document.getElementById('avatar-wrapper');

function triggerFace(emotion) {
    // Si estamos usando el modelo 3D
    if(noraModel) {
        try { noraModel.motion('TapBody'); } catch(e) {}
    } 
    // Si caímos al fallback SVG
    else {
        const fallbackImg = document.getElementById('fallback-avatar');
        if(fallbackImg) {
            fallbackImg.className = `avatar ${emotion}`;
        }
    }
}

function enableFallback() {
    console.warn("Usando avatar de respaldo (SVG) debido a bloqueos en el navegador.");
    avatarWrapper.innerHTML = `<img id="fallback-avatar" src="/static/avatar.svg" class="avatar neutral" style="width:200px; height:200px; filter: drop-shadow(0 0 15px rgba(88, 166, 255, 0.15)); margin-bottom: 20px;">`;
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

        // Hiyori (Cubism 4)
        const modelUrl = 'https://cdn.jsdelivr.net/gh/guansss/pixi-live2d-display/docs/assets/hiyori/hiyori_pro_t10.model3.json';

        PIXI.live2d.Live2DModel.from(modelUrl).then(model => {
            noraModel = model;
            app.stage.addChild(model);
            
            // Asegurarnos de que encaje en el canvas
            model.scale.set(0.13);
            model.x = 30;
            model.y = 50;

            document.addEventListener('mousemove', (e) => {
                model.focus(e.clientX, e.clientY);
            });
            
            model.on('pointertap', () => {
                model.motion('TapBody');
            });
        }).catch(err => {
            enableFallback();
        });
    } else {
        enableFallback();
    }
} catch (error) {
    enableFallback();
}
