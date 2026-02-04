Tentu, ini ide bagus. Menggunakan metode git clone membuat projectmu terlihat jauh lebih developer-friendly dan profesional.

Karena saya lihat di screenshot nama file kamu sudah berubah menjadi remotePort.py, saya sudah menyesuaikan instruksinya agar sinkron.

Berikut adalah README.md yang estetik, bersih, dan berfokus pada kemudahan penggunaan (Copy dan paste kode di bawah ini ke file README.md kamu):
Markdown

# 📺 CastControl-Py

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**CastControl-Py** is a minimalist automation tool to interact with Google Cast devices (Chromecast / Android TV) on your local network. It allows you to force-play media, manipulate volume, and manage app sessions remotely.

---

## ✨ Features

* **🔍 Auto-Discovery:** Automatically finds devices in your local network.
* **🔊 Volume Master:** Set specific volume levels or start a "strobe" volume loop.
* **📺 YouTube Force-Play:** Hijacks the TV session to play a specific video ID immediately.
* **💀 App Killer:** Remotely terminates active applications.

---

## 🚀 Installation & Usage

Follow these steps to set up the tool using **Git**:

### 1. Clone the Repository
Open your terminal and clone this project to your local machine:
```bash
git clone [https://github.com/HarsMX/Google-Cast-Remote-Controller-via-Python-.git](https://github.com/HarsMX/Google-Cast-Remote-Controller-via-Python-.git)
cd Google-Cast-Remote-Controller-via-Python-

2. Install Dependencies

Make sure you have Python installed, then install the required library:
Bash

pip install pychromecast

3. Run the Tool

Execute the script using Python:
Bash

python remotePort.py

📖 How to Use

    Enter IP: The script will ask for the Target IP (ensure port 8009 is open).

    Select Option:

        1 Volume Control: Set static volume or start a loop.

        2 Force YouTube: Enter a video ID/URL to force playback.

        3 Kill App: Stop the currently running application.

        4 Quit: Exit the tool.
