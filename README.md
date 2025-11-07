Got you. I’ll rewrite your README **clean, professional, and properly formatted** as one copy-paste-ready block.

Just replace your current `README.md` with the version below:

---

````markdown
# 🌍 AI Translator Pro

A modern, user-friendly translation app for **English ⇄ Swedish**.  
Powered by **Hugging Face Transformers**, **Edge-TTS**, and a sleek **Streamlit** interface.  

Translate text, listen to natural voice output, translate files, and track your translation history — all in one place.

---

## ✨ Key Features

| Feature | Description |
|--------|-------------|
| 🔄 **Bidirectional Translation** | Translate English ⇄ Swedish seamlessly |
| 🤖 **Helsinki-NLP Marian Models** | High-quality neural machine translation |
| 🎙️ **Natural Text-to-Speech (TTS)** | Uses Edge-TTS with adjustable speech speed |
| 📊 **Usage Analytics** | View translation count, average length, and total characters |
| 💾 **Download Everything** | Export audio, translated text, and session history (.csv) |
| 📁 **File Translation** | Upload `.txt` files and translate entire documents |
| 🕓 **Recent History Tracking** | Review or export your previous translations |

---

## 🖼️ App Preview

| Home Screen | Translation Result | File Translation |
|------------|------------------|-----------------|
| *(Example preview below)* | *(Second screen example)* | *(File translation example)* |

<img width="1910" alt="image" src="https://github.com/user-attachments/assets/5e397a93-5403-4711-8734-84dfd7442ac6" />

<img width="1909" alt="image" src="https://github.com/user-attachments/assets/4d2bfd36-34e3-4279-bc99-ceab9b1ef093" />

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/thessyrain/ai-translator-app.git
cd ai-translator-app
````

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run app.py
```

---

## 🧠 How It Works

| Component                   | Purpose                                  |
| --------------------------- | ---------------------------------------- |
| **MarianMT (Helsinki-NLP)** | Core neural machine translation          |
| **LangDetect**              | Automatically detects input language     |
| **Edge-TTS**                | Generates natural speech audio output    |
| **Streamlit**               | UI framework for interaction and display |
| **Pandas**                  | Stores and exports translation history   |

---

## 📂 Project Structure

```
ai-translator-app/
│
├── app.py               # Main application
├── requirements.txt     # Dependencies
├── README.md            # Documentation
└── screenshots/         # (Optional) UI images
```

---

## 🎧 Voice Output

| Language | Voice Used          |
| -------- | ------------------- |
| English  | `en-GB-SoniaNeural` |
| Swedish  | `sv-SE-SofieNeural` |

Voice speed can be adjusted in the sidebar.

---

## 🤝 Contributing

Contributions are welcome!

```bash
# Fork the repository
# Create your feature branch
git checkout -b feature-name

# Commit changes
git commit -m "Add new feature"

# Push the branch
git push origin feature-name
```

Open a Pull Request and describe your changes clearly.

---

## ⭐ Support the Project

If you find this useful:

* 🌟 Star the repository
* 🍴 Fork it
* 🐛 Suggest improvements via Issues

Your support helps it grow.

---

## 📜 License

This project is licensed under the **MIT License**.

---

Made with ❤️ by **@thessyrain**

```
Linkedin: https://www.linkedin.com/in/ibukunoluwaajibare/
---


