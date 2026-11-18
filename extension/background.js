const SERVER_URL = "http://127.0.0.1:5000/highlight";

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  const payload = {
    color: message.color,
    text: message.text,
    url: sender.tab.url,      // URL de l'onglet, pas de l'iframe
    title: sender.tab.title,  // titre de l'onglet
  };
  fetch(SERVER_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(message),
  })
    .then((response) => sendResponse({ ok: response.ok }))
    .catch(() => sendResponse({ ok: false }));

  return true; // garde la réponse ouverte (fetch est asynchrone)
});