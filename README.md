# DashNG 🚀

DashNG is a local web server application that lets you control **BeamNG** from any device on your network.  
You define a shortcut in BeamNG, give it a name on the web interface, and clicking it executes the key combination on the host PC.  
Perfect for having a mini dashboard instead of using the keyboard! 🎮💻

---

## 🛠️ Tech Stack

- **Front-end:** HTML, CSS, JavaScript  
- **Back-end:** Python

---

## ⚡ Features

- Define BeamNG shortcuts directly from the web interface  
- Execute key combinations on the host PC  
- Easy icon management (many default icons with option to upload your own)  
- Simple and responsive interface  

---

## 💾 Installation

1. Clone the repository

```bash
git clone https://github.com/userpetitpain/DashNG.git
cd DashNG
```

2. Install dependencies

For windows/macos
```bash
pip3 install -r requirement.txt
```

For linux
```bash
python3 -m venv venv # Create a virtual environnement
source venv/bin/activate
pip3 install -r requirement.txt
```

## Run the server

```bash
python3 app.py
```

Open your browser at :
[http://<your_pc_ip>:8000](http://127.0.0.1:8000)/run/media/zack2patate18/38c97c77-eaa9-4c2f-87c9-2552b819ceec/home/zack2patate/