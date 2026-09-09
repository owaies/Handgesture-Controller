# 🖐️ HandGesture Controller

> **Control PDF presentations with your hands.** Point, swipe, navigate, and enter an immersive presentation mode without touching the keyboard or mouse.

<p align="center">
  <a href="https://handgesturecontroller.netlify.app/"><img src="https://img.shields.io/badge/🚀%20Live%20Demo-HandGesture%20Controller-6366f1?style=for-the-badge" alt="Live Demo"></a>
  <a href="https://github.com/owaies/Handgesture-Controller"><img src="https://img.shields.io/github/stars/owaies/Handgesture-Controller?style=for-the-badge&logo=github" alt="GitHub stars"></a>
  <a href="https://github.com/owaies/Handgesture-Controller/network/members"><img src="https://img.shields.io/github/forks/owaies/Handgesture-Controller?style=for-the-badge&logo=github" alt="GitHub forks"></a>
  <a href="https://github.com/owaies/Handgesture-Controller/blob/main/LICENSE"><img src="https://img.shields.io/github/license/owaies/Handgesture-Controller?style=for-the-badge" alt="License"></a>
  <img src="https://img.shields.io/badge/AI-MediaPipe-blue?style=for-the-badge" alt="MediaPipe">
  <img src="https://img.shields.io/badge/PDF-pdf.js-red?style=for-the-badge" alt="PDF.js">
</p>

<p align="center">
  <strong>🎤 A browser-based AI presentation controller powered by MediaPipe Gesture Recognizer.</strong>
</p>

<p align="center">
  <a href="https://handgesturecontroller.netlify.app/"><strong>🌐 Try the Live Website →</strong></a>
</p>

---

## ✨ What is this?

**HandGesture Controller** turns your webcam into a touch-free presentation remote. Upload a PDF, enable your camera, and use recognized hand gestures to control the presentation and a virtual laser pointer.

The project runs directly in the browser using client-side JavaScript. There is no traditional backend required for the presentation experience.

### 🎯 Core capabilities

| Feature | What it does |
|---|---|
| 📄 **PDF presentation** | Upload a local PDF and render its pages in the browser |
| 🖐️ **Gesture recognition** | Uses MediaPipe Gesture Recognizer to interpret hand gestures |
| 🔴 **Laser pointer** | Use your index finger to control a virtual laser pointer |
| ⏭️ **Slide navigation** | Move forward and backward through PDF pages hands-free |
| 🖥️ **Immersive mode** | Hide the sidebar for a cleaner presentation view |
| 📷 **Webcam HUD** | Shows camera status and presentation state |
| ⚡ **No build step** | The app is a standalone HTML experience |

---

## 🌐 Live Demo

### 🚀 [Launch HandGesture Controller](https://handgesturecontroller.netlify.app/)

Open the deployed application directly in your browser:

**https://handgesturecontroller.netlify.app/**

> 📷 Camera access is required for gesture recognition. For the best experience, use a modern browser over HTTPS and allow camera permission when prompted.

---

## 🕹️ Gesture Controls

<details open>
<summary><strong>Show gesture map</strong></summary>

<br>

| Gesture | Action | Icon |
|---|---|---|
| ☝️ **Index Finger** | Control the laser pointer | 🔴 |
| ✌️ **Victory** | Next slide | ➡️ |
| 👍 **Thumb Up** | Previous slide | ⬅️ |
| ✋ **Open Palm** | Toggle immersive/fullscreen-style presentation mode | 🖥️ |

> **Tip:** Keep your hand clearly visible to the webcam and allow the gesture recognizer a moment to detect it before making another presentation gesture.

</details>

---

## 🚀 Quick Start

<details open>
<summary><strong>1. Try the live website</strong></summary>

<br>

Visit **[handgesturecontroller.netlify.app](https://handgesturecontroller.netlify.app/)** and start presenting immediately.

</details>

<details>
<summary><strong>2. Run locally</strong></summary>

<br>

Clone the repository:

```bash
git clone https://github.com/owaies/Handgesture-Controller.git
cd Handgesture-Controller
```

Because the project is a static HTML application, you can serve it with any simple local HTTP server.

**Python:**

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/index%20(1).html
```

</details>

<details>
<summary><strong>3. Start presenting</strong></summary>

<br>

1. 📄 Upload a PDF.
2. 📷 Click **Start Camera**.
3. 🤚 Allow camera permission when prompted.
4. 🧠 Wait for **AI Active**.
5. 🖐️ Use the gesture controls above.
6. 🎤 Present without touching the computer.

</details>

---

## 🧠 How It Works

```text
┌─────────────────┐
│   Local PDF     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐       ┌────────────────────┐
│     PDF.js      │       │      Webcam        │
│  Render pages   │       │   Video stream     │
└────────┬────────┘       └─────────┬──────────┘
         │                          │
         │                          ▼
         │                ┌────────────────────┐
         │                │     MediaPipe      │
         │                │ Gesture Recognizer │
         │                └─────────┬──────────┘
         │                          │
         │              ┌───────────┴───────────┐
         │              │                       │
         ▼              ▼                       ▼
┌────────────────┐  ┌───────────┐        ┌──────────────┐
│ Canvas display │  │ Gestures  │        │ Laser cursor │
└────────────────┘  └─────┬─────┘        └──────────────┘
                          │
                 ┌────────┴────────┐
                 ▼        ▼        ▼
              Next     Previous  Immersive
              Slide     Slide      Mode
```

### 🔍 Technology flow

- **PDF.js** loads the selected PDF in the browser and renders the active page onto a canvas.
- **MediaPipe Tasks Vision** provides the gesture-recognition model and webcam inference pipeline.
- The browser's **MediaDevices API** requests webcam access.
- JavaScript maps recognized gestures to presentation actions.
- The **laser pointer** follows the detected pointing position on the presentation stage.

---

## 🧩 Tech Stack

| Technology | Role |
|---|---|
| **HTML5** | Application structure |
| **CSS3** | UI, HUD, animations, immersive layout |
| **JavaScript (ES Modules)** | Application logic |
| **MediaPipe Tasks Vision** | AI hand gesture recognition |
| **PDF.js** | PDF loading and rendering |
| **Font Awesome** | Interface icons |
| **Web APIs** | Camera and browser capabilities |

External libraries are loaded from CDN at runtime.

---

## 📁 Project Structure

```text
Handgesture-Controller/
├── 📄 README.md
└── 🌐 index (1).html
```

The main application is intentionally compact and contained in a single HTML file, including its styling and JavaScript logic.

---

## 🔐 Privacy

The presentation uses your browser's camera permission to perform gesture recognition. Before using the application, make sure you are comfortable granting camera access to the page.

Your PDF is selected locally through the browser and rendered for the presentation experience. The repository itself does not require you to upload the PDF to a project backend.

> **Good practice:** Use the app over HTTPS when deployed publicly. Browsers commonly require a secure context for camera access, with `localhost` treated as a trusted development context.

---

## 🌐 Browser Requirements

For the best experience, use a modern browser with support for:

- ✅ WebRTC / `getUserMedia()`
- ✅ ES modules
- ✅ HTML Canvas
- ✅ Modern JavaScript
- ✅ WebAssembly, used by MediaPipe Tasks Vision
- ✅ A working webcam for gesture control

A Chromium-based browser such as recent Chrome or Edge is a practical choice for testing.

---

## 🛠️ Troubleshooting

<details>
<summary><strong>📷 Camera does not start</strong></summary>

Make sure:

- Camera permission is allowed for the page.
- No other application is exclusively using the webcam.
- You are running from `localhost` or an HTTPS deployment.
- Your browser supports `navigator.mediaDevices.getUserMedia()`.

</details>

<details>
<summary><strong>🧠 AI stays loading</strong></summary>

The gesture model is loaded from external MediaPipe/CDN resources. Check your internet connection and browser developer console for blocked network requests.

</details>

<details>
<summary><strong>📄 PDF does not render</strong></summary>

Make sure the selected file is a valid PDF. Try another PDF if the document appears corrupted or unusually complex.

</details>

<details>
<summary><strong>🖐️ Gestures are not detected reliably</strong></summary>

Try:

- Improving room lighting.
- Keeping your hand fully inside the camera frame.
- Holding gestures clearly for a moment.
- Moving farther from the camera if your hand is too close to the lens.
- Avoiding busy backgrounds where possible.

</details>

---

## 🧪 Development

The project currently has no package manager or build pipeline. To modify it:

1. Edit `index (1).html`.
2. Serve the repository locally.
3. Open the app in a modern browser.
4. Test PDF rendering.
5. Test each gesture with the webcam.
6. Check the browser console for runtime errors.

### Useful test checklist

- [ ] PDF uploads correctly
- [ ] First page renders
- [ ] Next-slide gesture works
- [ ] Previous-slide gesture works
- [ ] Laser pointer tracks the pointing hand
- [ ] Immersive mode toggles
- [ ] Camera can be stopped and restarted
- [ ] Another PDF can be loaded
- [ ] UI remains usable at different viewport sizes

---

## 💡 Ideas for Future Versions

- 🎮 Custom gesture mapping
- ⌨️ Keyboard fallback controls
- 📱 Better mobile/tablet presentation support
- 🖱️ Configurable laser pointer size and color
- 📊 Gesture confidence indicators
- 📝 Presenter notes
- 🎙️ Voice commands
- 🖼️ Presentation thumbnails
- 🌙 Additional visual themes
- 📈 Gesture/event analytics for debugging

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the application with a real webcam.
5. Open a pull request with a clear description of the change.

For significant changes, consider opening an issue first so the approach can be discussed.

---

## 📜 License

No license file is currently present in the repository. If you intend others to reuse, modify, or redistribute the project, consider adding an explicit open-source license.

---

## 👨‍💻 Author

**Owaies**

- GitHub: [@owaies](https://github.com/owaies)
- Repository: [Handgesture-Controller](https://github.com/owaies/Handgesture-Controller)
- Live Demo: [handgesturecontroller.netlify.app](https://handgesturecontroller.netlify.app/)

---

<p align="center">
  <strong>🖐️ Present. Point. Control.</strong><br>
  Built for touch-free presentations with browser-based AI.
</p>
