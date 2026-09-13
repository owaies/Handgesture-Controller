# 🖐️ HandGesture Controller

> **Control PDF presentations with your hands.** Point, swipe, navigate, and enter an immersive presentation mode without touching the keyboard or mouse.

<p align="center">
  <a href="https://handgesturecontroller.netlify.app/"><img src="https://img.shields.io/badge/🚀%20Live%20Demo-HandGesture%20Controller-6366f1?style=for-the-badge" alt="Live Demo"></a>
  <a href="https://github.com/owaies/Handgesture-Controller"><img src="https://img.shields.io/github/stars/owaies/Handgesture-Controller?style=for-the-badge&logo=github" alt="GitHub stars"></a>
</p>

<p align="center"><strong>🎤 A browser-based AI presentation controller powered by MediaPipe Gesture Recognizer.</strong></p>

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

## 🕹️ Gesture Controls

| Gesture | Action |
|---|---|
| ☝️ **Index Finger** | Laser Pointer |
| ✌️ **Victory** | Next Slide |
| 👍 **Thumb Up** | Previous Slide |
| ✋ **Open Palm** | Fullscreen presentation |

---

## 🚀 Deployment

The application is a static HTML experience and can be deployed directly to Vercel or any static host.

**Vercel production:** https://handgesture-controller.vercel.app/

---

## 🛠️ Development

```bash
git clone https://github.com/owaies/Handgesture-Controller.git
cd Handgesture-Controller
python -m http.server 8000
```

Then open `http://localhost:8000/index.html`.

---

## 📜 License

No license file is currently present in the repository.

---

## 👨‍💻 Author

**Owaies**

- GitHub: [@owaies](https://github.com/owaies)
- Repository: [Handgesture-Controller](https://github.com/owaies/Handgesture-Controller)

---

<p align="center"><strong>🖐️ Present. Point. Control.</strong></p>
