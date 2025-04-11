const msgInput = document.getElementById("msg");
const chatLog = document.getElementById("chatLog");
const toggleBtn = document.getElementById("toggle-theme");
let darkMode = false;

function formatTime() {
  const now = new Date();
  return now.toLocaleTimeString("ko-KR", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function renderMessage(sender, text, isUser = false, loading = false) {
  const wrapper = document.createElement("div");
  wrapper.className = `msg-bubble ${isUser ? "user" : "bot"}`;
  wrapper.innerHTML = `
    <div class="sender">${sender}</div>
    <div class="text">${
      loading ? "<span class='loading'>입력 중...</span>" : text
    }</div>
    <div class="timestamp">${formatTime()}</div>
  `;
  chatLog.appendChild(wrapper);
  chatLog.scrollTop = chatLog.scrollHeight;
  console.info(`${sender} ▶️`, text);
}

function send() {
  const message = msgInput.value.trim();
  if (!message) return;

  renderMessage("🙋‍♂️", message, true);
  msgInput.value = "";

  renderMessage("🤖", "", false, true);

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  })
    .then((res) => res.json())
    .then((data) => {
      chatLog.removeChild(chatLog.lastChild);
      renderMessage("🤖", data.reply, false);
    });
}

msgInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    send();
  }
});

toggleBtn.addEventListener("click", () => {
  darkMode = !darkMode;
  document.body.classList.toggle("dark-mode");
  toggleBtn.innerText = darkMode ? "☀️" : "🌙";
  console.log("🌗 다크모드:", darkMode);
});
