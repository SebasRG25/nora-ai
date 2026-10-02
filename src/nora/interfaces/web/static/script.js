const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const avatar = document.getElementById('nora-avatar');

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
    
    // Desactivar input y animar que está pensando
    sendBtn.disabled = true;
    avatar.className = 'avatar thinking';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: text})
        });
        
        const data = await response.json();
        
        // Poner la animación que NORA eligió
        avatar.className = `avatar ${data.face}`;
        
        // Volver a neutral después de 2 segundos si no es neutral
        if(data.face !== 'neutral') {
            setTimeout(() => {
                avatar.className = 'avatar neutral';
            }, 3000);
        }
        
        addMessage('nora', data.response);
        
    } catch (error) {
        addMessage('nora', 'Error de conexión cognitiva.');
        avatar.className = 'avatar neutral';
    } finally {
        sendBtn.disabled = false;
        userInput.focus();
    }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
