const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const messages = document.getElementById("messages");
const sendButton = document.getElementById("send-button");
const statusText = document.getElementById("status");

function addMessage(text, sender, matchedQuestion = null) {
  const row = document.createElement("div");
  row.className = `message-row ${sender === "user" ? "user-row" : "bot-row"}`;

  const avatar = document.createElement("div");
  avatar.className = "tiny-avatar";
  avatar.textContent = sender === "user" ? "Y" : "A";

  const content = document.createElement("div");
  const bubble = document.createElement("div");
  bubble.className = `bubble ${sender === "user" ? "user-bubble" : "bot-bubble"}`;
  bubble.textContent = text;
  content.appendChild(bubble);

  if (matchedQuestion) {
    const match = document.createElement("div");
    match.className = "match-label";
    match.textContent = `Matched FAQ: ${matchedQuestion}`;
    content.appendChild(match);
  }

  row.appendChild(avatar);
  row.appendChild(content);
  messages.appendChild(row);
  messages.scrollTop = messages.scrollHeight;
}

async function sendMessage(message) {
  const cleanMessage = message.trim();
  if (!cleanMessage) return;

  addMessage(cleanMessage, "user");
  input.value = "";
  input.focus();
  sendButton.disabled = true;
  statusText.textContent = "Finding the best matching FAQ...";

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: cleanMessage })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "The chatbot could not answer right now.");
    addMessage(data.answer, "bot", data.matched_question);
    statusText.textContent = data.matched_question
      ? `Best match confidence: ${Math.round(data.confidence * 100)}%`
      : "Try another way of asking, or add more FAQs.";
  } catch (error) {
    addMessage(error.message || "Unable to connect to the chatbot API. Check that the backend is running.", "bot");
    statusText.textContent = "Connection error";
  } finally {
    sendButton.disabled = false;
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(input.value);
});

document.querySelectorAll(".suggestion").forEach((button) => {
  button.addEventListener("click", () => sendMessage(button.textContent));
});

document.getElementById("clear-chat").addEventListener("click", () => {
  messages.replaceChildren();
  addMessage("Hi there! 👋 I'm your FAQ assistant. What would you like to know?", "bot");
  statusText.textContent = "Powered by TF-IDF and cosine similarity";
  input.focus();
});
