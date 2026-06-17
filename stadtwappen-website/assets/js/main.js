const navToggle = document.querySelector('.nav-toggle');
const mainNav = document.querySelector('.main-nav');

if (navToggle && mainNav) {
  navToggle.addEventListener('click', () => {
    const open = mainNav.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', String(open));
  });
}

document.querySelectorAll('.main-nav a').forEach((link) => {
  link.addEventListener('click', () => {
    if (mainNav) mainNav.classList.remove('is-open');
    if (navToggle) navToggle.setAttribute('aria-expanded', 'false');
  });
});

const lightbox = document.querySelector('.lightbox');
const lightboxImg = document.querySelector('.lightbox img');
const lightboxClose = document.querySelector('.lightbox button');

document.querySelectorAll('[data-lightbox]').forEach((item) => {
  item.addEventListener('click', (event) => {
    event.preventDefault();
    if (!lightbox || !lightboxImg) return;
    lightboxImg.src = item.getAttribute('href');
    lightbox.classList.add('is-open');
  });
});

function closeLightbox() {
  if (lightbox) lightbox.classList.remove('is-open');
  if (lightboxImg) lightboxImg.src = '';
}

if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
if (lightbox) {
  lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox) closeLightbox();
  });
}
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeLightbox();
});

const consentKey = 'stadtwappen-cookie-consent';

function hasConsent() {
  try {
    return localStorage.getItem(consentKey) === 'accepted';
  } catch {
    return false;
  }
}

function saveConsent() {
  try {
    localStorage.setItem(consentKey, 'accepted');
  } catch {
    // If storage is unavailable, keep the consent for the current page view.
  }
}

function loadMapEmbeds() {
  document.querySelectorAll('.map-card iframe[data-src]').forEach((iframe) => {
    iframe.src = iframe.dataset.src;
    iframe.removeAttribute('data-src');
    const card = iframe.closest('.map-card');
    if (card) {
      card.classList.remove('is-pending');
      card.querySelector('.map-consent')?.remove();
    }
  });
}

function acceptCookies() {
  saveConsent();
  loadMapEmbeds();
  document.querySelector('.cookie-banner')?.remove();
}

function setupMapConsent() {
  document.querySelectorAll('.map-card iframe[data-src]').forEach((iframe) => {
    const card = iframe.closest('.map-card');
    if (!card || card.querySelector('.map-consent')) return;

    card.classList.add('is-pending');
    const notice = document.createElement('div');
    notice.className = 'map-consent';
    notice.innerHTML = `
      <div>
        <strong>Google Maps anzeigen</strong>
        <p>Beim Laden der Karte werden Daten an Google übertragen. Details finden Sie in der <a href="datenschutz.html">Datenschutzerklärung</a>.</p>
      </div>
      <button type="button">Karte laden</button>
    `;
    notice.querySelector('button').addEventListener('click', acceptCookies);
    card.append(notice);
  });
}

function showCookieBanner() {
  if (hasConsent() || document.querySelector('.cookie-banner')) return;

  const banner = document.createElement('div');
  banner.className = 'cookie-banner';
  banner.setAttribute('role', 'dialog');
  banner.setAttribute('aria-label', 'Cookie-Hinweis');
  banner.innerHTML = `
    <p>Wir verwenden technisch notwendige Speicherfunktionen und laden externe Inhalte wie Google Maps erst nach Ihrer Zustimmung. Weitere Informationen finden Sie in unserer <a href="datenschutz.html">Datenschutzerklärung</a>.</p>
    <button type="button">Akzeptieren</button>
  `;
  banner.querySelector('button').addEventListener('click', acceptCookies);
  document.body.append(banner);
}

if (hasConsent()) {
  loadMapEmbeds();
} else {
  setupMapConsent();
  showCookieBanner();
}
