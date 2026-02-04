# 📺 CastControl-Py
A minimalist Python tool to interact, automate, and control Google Cast devices within a local network.

## ✨ Features
* **Device Info:** Extract UUID, Model, and Manufacturer.
* **Volume Master:** Standard volume setting & auto-looping volume stress test.
* **YouTube Force-Play:** Automates app launching and video playback using a double-tap strategy for reliability.
* **Session Manager:** Remotely quit active applications.

## 🛠 Prerequisites
Ensure the target device has ports `8008` and `8009` open (Check via Nmap).

```bash
pip install pychromecast
