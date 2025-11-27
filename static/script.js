const form = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const userInput = document.getElementById("user_input").value.trim();
    if (!userInput) return;

    // Display user message
    const userMsgDiv = document.createElement("div");
    userMsgDiv.classList.add("user-message");
    userMsgDiv.textContent = userInput;
    chatBox.appendChild(userMsgDiv);

    // Clear input
    document.getElementById("user_input").value = "";

    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    // Send AJAX request
    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `user_input=${encodeURIComponent(userInput)}`
        });
        const data = await response.json();

        const botMsgDiv = document.createElement("div");
        botMsgDiv.classList.add("bot-message");
        botMsgDiv.textContent = data.answer || "Sorry, I could not answer that.";
        chatBox.appendChild(botMsgDiv);

        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (err) {
        console.error(err);
        const botMsgDiv = document.createElement("div");
        botMsgDiv.classList.add("bot-message");
        botMsgDiv.textContent = "❌ Error connecting to server.";
        chatBox.appendChild(botMsgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
