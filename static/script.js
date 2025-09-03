function sendMessage() {
    let userInput = document.getElementById("userInput").value;
    if (!userInput) return;

    let chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<div class="message user"><b>You:</b> ${userInput}</div>`;
    
    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        chatbox.innerHTML += `<div class="message bot"><b>Bot:</b> ${data.reply}</div>`;
        chatbox.scrollTop = chatbox.scrollHeight;
    });

    document.getElementById("userInput").value = "";
}
function sendMessage() {
    let userInput = document.getElementById("userInput").value;
    if (!userInput) return;

    let chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<div class="message user"><b>You:</b> ${userInput}</div>`;
    
    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        chatbox.innerHTML += `<div class="message bot"><b>Bot:</b> ${data.reply}</div>`;
        chatbox.scrollTop = chatbox.scrollHeight;
    });

    document.getElementById("userInput").value = "";
}
