# Step-by-Step: Webseite „Gaststätte zum Stadtwappen“ veröffentlichen

Dieses Paket ist eine fertige statische Webseite im Design des Mockups:

- `index.html` – Startseite
- `speisekarte.html` – Speisekarte mit vorbereiteten Bereichen
- `saisonkarte.html` – Saisonkarte
- `feiern.html` – Feiern & Veranstaltungen
- `galerie.html` – Bildergalerie mit Lightbox
- `kontakt.html` – Kontakt, Öffnungszeiten, Karte-Link
- `impressum.html` – vorbereitete Impressumsseite
- `datenschutz.html` – vorbereitete Datenschutzseite
- `assets/css/styles.css` – komplettes Design
- `assets/js/main.js` – mobiles Menü + Galerie-Lightbox
- `assets/images/` – alle Bilder aus dem Design

---

## 1. Lokal anschauen

### Variante A: Einfach per Doppelklick
1. ZIP entpacken.
2. `index.html` im Browser öffnen.
3. Navigation testen.

### Variante B: Lokal mit Mini-Webserver testen
Im entpackten Ordner ausführen:

```bash
python3 -m http.server 8080
```

Dann im Browser öffnen:

```text
http://localhost:8080
```

---

## 2. Inhalte anpassen

### Öffnungszeiten ändern
Dateien öffnen:

- `index.html`
- `kontakt.html`

Suche nach:

```html
10:30–14:00 Uhr
16:30–22:00 Uhr
```

und ersetze die Zeiten.

### Telefon ändern
Suche in den HTML-Dateien nach:

```html
0911 / 77 11 15
0911 / 77 19 97
```

Wichtig: Bei `tel:` muss die Nummer ohne Leerzeichen stehen:

```html
href="tel:+49911771115"
```

### Speisekarte ändern
Datei:

```text
speisekarte.html
```

Suche nach Blöcken wie:

```html
<div class="menu-item">
  <div>
    <strong>Schäufele mit Kloß</strong>
    <small>Knusprige Kruste, dunkle Soße, fränkischer Kartoffelkloß.</small>
  </div>
  <span class="menu-price">—</span>
</div>
```

Preis eintragen:

```html
<span class="menu-price">16,90 €</span>
```

---

## 3. Bilder austauschen

Alle Bilder liegen hier:

```text
assets/images/
```

Wichtig: Wenn du ein Bild 1:1 ersetzen willst, behalte einfach den Dateinamen bei.

Beispiel:

```text
assets/images/hero-schaeufele.jpg
```

ersetzen durch eigenes Foto mit gleichem Namen.

Empfohlene Bildgrößen:

- Hero-Bild: mindestens 1920 × 1080 px
- Galerie/Speisen: mindestens 1200 × 900 px
- Logo/Wappen: möglichst PNG/JPG mit sauberem Hintergrund

---

## 4. Vor Veröffentlichung prüfen

Bitte unbedingt kontrollieren:

1. Telefonnummern stimmen?
2. Öffnungszeiten stimmen?
3. Speisekarte und Preise stimmen?
4. Impressum vollständig?
5. Datenschutz vollständig?
6. Sind die KI-Bilder für euren echten Restaurant-Auftritt okay oder sollen echte Fotos rein?

---

## 5. Alte Webseite sichern

Bevor du etwas hochlädst:

1. Per FTP/SFTP beim Hosting anmelden.
2. Aktuellen Webordner herunterladen, z. B. `public_html`, `httpdocs`, `www` oder ähnlich.
3. Lokal als Backup speichern, z. B.:

```text
backup-alte-webseite-2026-06-17/
```

---

## 6. Webseite hochladen

In den Webordner des Hostings hochladen:

```text
index.html
speisekarte.html
saisonkarte.html
feiern.html
galerie.html
kontakt.html
impressum.html
datenschutz.html
assets/
```

Wichtig: Die Ordnerstruktur muss exakt gleich bleiben:

```text
assets/css/styles.css
assets/js/main.js
assets/images/...
```

---

## 7. Nach Upload testen

Im Browser öffnen:

```text
https://stadtwappen-fuerth.de/
```

Dann prüfen:

- Desktop-Ansicht
- Handy-Ansicht
- Menü-Button auf Handy
- Galerie anklicken
- Telefonnummer anklicken
- Google-Maps-Link anklicken
- Impressum und Datenschutz öffnen

---

## 8. Häufige Probleme

### Bilder werden nicht angezeigt
Meistens liegt es an falscher Ordnerstruktur. Prüfen:

```text
assets/images/hero-schaeufele.jpg
```

muss wirklich genau dort liegen.

### Design fehlt komplett
Dann fehlt wahrscheinlich diese Datei:

```text
assets/css/styles.css
```

### Handy-Menü geht nicht
Dann fehlt wahrscheinlich:

```text
assets/js/main.js
```

### Startseite zeigt noch alte Webseite
Browsercache leeren oder testen mit:

```text
https://stadtwappen-fuerth.de/?neu=1
```

---

## 9. Wichtiger Produktionshinweis

Die enthaltenen Bilder sind KI-generierte Platzhalter im gewünschten Stil. Für die echte Restaurant-Webseite sind echte Fotos vom Lokal, von euren Gerichten und euren Räumen besser und vertrauenswürdiger. Das Design ist so gebaut, dass du die Bilder einfach austauschen kannst, ohne HTML/CSS neu zu schreiben.
