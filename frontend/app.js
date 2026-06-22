const chat = document.getElementById("chat");
const form = document.getElementById("form");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");

const history = [];

function addMessage(text, role) {
  const el = document.createElement("div");
  el.className = `msg ${role}`;
  el.textContent = text;
  chat.appendChild(el);
  chat.scrollTop = chat.scrollHeight;
  return el;
}

addMessage(
  "Hi! I'm Fatima's Assistant. Ask me about education, skills, projects, or experience from the CV.",
  "bot"
);

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = input.value.trim();
  if (!question) return;

  addMessage(question, "user");
  input.value = "";
  input.disabled = true;
  sendBtn.disabled = true;

  const loading = addMessage("Thinking...", "loading");

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: question, history }),
    });

    if (!res.ok) throw new Error("Request failed");

    const data = await res.json();
    loading.remove();
    addMessage(data.answer, "bot");

    history.push({ role: "user", content: question });
    history.push({ role: "assistant", content: data.answer });
  } catch {
    loading.remove();
    addMessage("Something went wrong. Is the server running?", "bot");
  } finally {
    input.disabled = false;
    sendBtn.disabled = false;
    input.focus();
  }
});
