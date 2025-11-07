
# 🌍 AI Translator Pro

AI Translator Pro is a simple, intuitive, and reliable translation tool designed to help you translate **English ↔ Swedish** with ease.  
Whether you're learning the language, communicating professionally, or translating everyday text, this app offers accurate translation and natural voice playback that sounds clear and pleasant.

The experience is clean, fast, and straightforward — no clutter, no complexity.

---

## Why This App Exists

Language translation tools can sometimes feel overwhelming or impersonal.  
This project focuses on being **practical and friendly**:

- Easy to use  
- Clean interface  
- Accurate translations  
- Natural voice output you can actually understand  

It’s great for students, new arrivals in Sweden, professionals, and everyday communication.

---

## What You Can Do

| Feature | Description |
|--------|-------------|
| 🔄 Translate Both Ways | English → Swedish or Swedish → English automatically |
| 🗣️ Listen to Your Translation | Clear, natural voice audio with adjustable speed |
| 📄 Translate Document Text | Upload a `.txt` file and translate the entire content |
| 📊 Track Your Usage | See how much you’ve translated over time |
| 💾 Save Your Work | Download translated text or export session history (.csv) |
| 🕓 Access Your Recent Translations | Quickly revisit past translations |

---

## Preview

**Main Translator View**

[<img width="1910" src="https://github.com/user-attachments/assets/5e397a93-5403-4711-8734-84dfd7442ac6" />](https://github.com/thessyrain/ai-translator-app/blob/main/Screenshot%202025-11-07%20134715.png)


**Translation & Voice Output Example**

https://github.com/thessyrain/ai-translator-app/blob/main/Translator%20Video.mp4


---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/thessyrain/ai-translator-app.git
cd ai-translator-app
````

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

```bash
# macOS / Linux
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

Your browser will open automatically.

---

## How It Works

| Component                      | Role                                    |
| ------------------------------ | --------------------------------------- |
| **Helsinki-NLP Marian Models** | Performs the translation                |
| **Edge-TTS**                   | Generates natural spoken audio          |
| **LangDetect**                 | Detects the language of your input text |
| **Streamlit**                  | Provides the interactive web interface  |
| **Pandas**                     | Manages translation history             |

---

## Project Structure

```
ai-translator-app/
│
├── app.py               # Main application logic
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## Contributing

If you’d like to contribute—whether by improving translation features, UI enhancements, or support for new languages—your ideas are welcome.

* Open an Issue
* Submit a Pull Request
* Start a Discussion

Collaboration is genuinely appreciated.

---

## Connect

If you'd like to connect professionally or discuss collaboration, feel free to reach out:

**LinkedIn:** [https://www.linkedin.com/in/ibukunoluwaajibare/](https://www.linkedin.com/in/ibukunoluwaajibare/)

---

## License

This project is released under the **MIT License**.
You're free to use it, learn from it, adapt it, and share it.

---

Made with care, curiosity, and a love for language learning.
**By @thessyrain**





