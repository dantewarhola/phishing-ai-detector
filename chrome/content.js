// chrome/content.js

console.log("📨 Phish‑AI content script injected");

// === Configuration: tweak these as you retrain your model ===
const PHISHING_MAX    = 50;  // score ≤ this ⇒ phishing
const UNSURE_MAX      = 75;  // score ≤ this ⇒ unsure
// score > UNSURE_MAX ⇒ safe

// Inject or update the banner
function injectBanner(msg, bgColor) {
  // Remove any old banner
  document.querySelectorAll('.phish-ai-banner').forEach(el => el.remove());

  const banner = document.createElement('div');
  banner.className = 'phish-ai-banner';
  banner.textContent = msg;
  banner.style.cssText = `
    background: ${bgColor};
    color: white;
    font-size: 16px;
    font-weight: bold;
    padding: 8px;
    text-align: center;
    margin-bottom: 8px;
  `;

  // Prepend inside the main message pane
  const emailPane = document.querySelector('div[role="main"]');
  if (emailPane) {
    emailPane.prepend(banner);
    console.log("📢 Phish‑AI banner injected:", msg);
  }
}

// Remove banner when no email body is present
function clearBannerIfNoEmail() {
  const bodyEls = document.querySelectorAll('div.a3s, div.ii.gt');
  const open = Array.from(bodyEls).some(el => el.offsetParent !== null);
  if (!open) {
    document.querySelectorAll('.phish-ai-banner').forEach(el => el.remove());
    console.log("🧹 Phish‑AI banner cleared (no open email)");
  }
}

// Called whenever Gmail’s DOM changes
const observer = new MutationObserver(() => {
  // First, clear banner if we’re back to the inbox/list view
  clearBannerIfNoEmail();

  // Then, if an email is open, fetch and inject
  const bodyEls = document.querySelectorAll('div.a3s, div.ii.gt');
  const emailBodyDiv = Array.from(bodyEls).find(el => el.offsetParent !== null);
  if (!emailBodyDiv) return;

  const emailText = emailBodyDiv.innerText;
  console.log("Phish‑AI: detected email text length", emailText.length);

  // Ask the background worker to do the mixed‑content‑safe fetch
  chrome.runtime.sendMessage(
    { type: 'PHISH_AI_PREDICT', text: emailText },
    (response) => {
      if (!response || !response.success) {
        console.error('Phish‑AI extension error:', response && response.error);
        return;
      }
      const { score } = response.data;
      const pct = Math.round(score * 100);
      let msg, color;

      if (pct <= PHISHING_MAX)      { msg = `⚠️ Phishing (${pct}%)`; color = '#d32f2f'; }
      else if (pct <= UNSURE_MAX)   { msg = `🤔 Unsure (${pct}%)`;   color = '#f9a825'; }
      else                           { msg = `✅ Safe (${pct}%)`;     color = '#388e3c'; }

      injectBanner(msg, color);
    }
  );
});

// Start observing Gmail’s dynamic content
observer.observe(document.body, { childList: true, subtree: true });
