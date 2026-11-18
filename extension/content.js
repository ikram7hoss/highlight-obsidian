const COLORS = {
  yellow: "#ffe066",
  green: "#8ce99a",
  blue: "#74c0fc",
  red: "#ff8787",
  purple: "#b197fc",
};

let bar = null;

function removeBar() {
  if (bar) {
    bar.remove();
    bar = null;
  }
}

function showBar(x, y, text) {
  removeBar();
  bar = document.createElement("div");
  bar.style.cssText = `
    position: absolute; left: ${x}px; top: ${y}px; z-index: 2147483647;
    display: flex; gap: 6px; padding: 6px;
    background: #333; border-radius: 8px;
  `;

  for (const [color, hex] of Object.entries(COLORS)) {
    const button = document.createElement("button");
    button.style.cssText = `
      width: 22px; height: 22px; border-radius: 50%;
      border: none; cursor: pointer; background: ${hex};
    `;
    // mousedown + preventDefault : garde le texte sélectionné
    button.addEventListener("mousedown", (e) => e.preventDefault());
    button.addEventListener("click", () => send(color, text, button));
    bar.appendChild(button);
  }

  document.body.appendChild(bar);
}

function send(color, text, button) {
  chrome.runtime.sendMessage(
    { color, text, url: location.href, title: document.title },
    (response) => {
      button.textContent = response && response.ok ? "✓" : "✗";
      setTimeout(removeBar, 700);
    }
  );
}

document.addEventListener("mouseup", (e) => {
  if (bar && bar.contains(e.target)) return; // clic dans la barre : on ne fait rien

  setTimeout(() => {
    const selection = window.getSelection();
    const text = selection.toString().trim();
    if (!text) {
      removeBar();
      return;
    }
    const rect = selection.getRangeAt(0).getBoundingClientRect();
    showBar(
      rect.left + window.scrollX,
      rect.bottom + window.scrollY + 6,
      text
    );
  }, 10);
});