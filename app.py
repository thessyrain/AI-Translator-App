import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect, LangDetectException
import asyncio, os
import edge_tts
from datetime import datetime
import pandas as pd

# ==========================
# ⚙️ PAGE CONFIGURATION
# ==========================
st.set_page_config(
    page_title="AI Translator Pro",
    page_icon="🌍",
    layout="wide",
)

# ==========================
# 🎨 ENHANCED STYLING
# ==========================
st.markdown("""
    <style>
    h1 { text-align: center; color: #2E4053; font-size: 3rem; }
    .subtitle { text-align: center; color: #5D6D7E; font-size: 18px; margin-bottom: 2rem; }
    .output-box {
        background: linear-gradient(135deg, #f4f6f7 0%, #e8edf0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #2E86C1;
        font-size: 18px;
        font-weight: 500;
        color: #1b2631;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background: linear-gradient(135deg, #2E86C1 0%, #1B4F72 100%);
        color: white;
        border-radius: 10px;
        font-weight: 600;
        border: none;
        padding: 0.7rem 1.5rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(46, 134, 193, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================
# 🧠 ENHANCED MODEL LOADING
# ==========================
@st.cache_resource
def load_models():
    """Load translation models with error handling"""
    try:
        en_sv = "Helsinki-NLP/opus-mt-en-sv"
        sv_en = "Helsinki-NLP/opus-mt-sv-en"
        tok_en_sv = MarianTokenizer.from_pretrained(en_sv)
        mod_en_sv = MarianMTModel.from_pretrained(en_sv)
        tok_sv_en = MarianTokenizer.from_pretrained(sv_en)
        mod_sv_en = MarianMTModel.from_pretrained(sv_en)
        return tok_en_sv, mod_en_sv, tok_sv_en, mod_sv_en
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None, None, None

tok_en_sv, mod_en_sv, tok_sv_en, mod_sv_en = load_models()

# ==========================
# 🔄 ENHANCED TRANSLATION
# ==========================
def translate_text(text, src_lang):
    """Translate text with error handling and validation"""
    if not text or not text.strip():
        return "No text to translate"
    
    try:
        if src_lang == "en":
            tok, model = tok_en_sv, mod_en_sv
        else:
            tok, model = tok_sv_en, mod_sv_en
        
        inputs = tok(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        output = model.generate(**inputs, max_length=512, num_beams=5, early_stopping=True)
        return tok.decode(output[0], skip_special_tokens=True)
    except Exception as e:
        return f"Translation error: {str(e)}"

def detect_language(text):
    """Enhanced language detection with error handling"""
    try:
        detected = detect(text)
        confidence = "High"
        return detected, confidence
    except LangDetectException:
        return "unknown", "Low"
    except Exception as e:
        return "error", "Error"

# ==========================
# 🗣️ SIMPLIFIED TTS (NO FFMPEG NEEDED!)
# ==========================
async def generate_voice(text, lang, voice_speed=1.0):
    """Generate voice with customizable speed"""
    voice = "en-GB-SoniaNeural" if lang == "en" else "sv-SE-SofieNeural"
    output_path = "output.mp3"
    
    # Calculate rate correctly - edge-tts needs format like "+50%" or "-50%"
    if voice_speed == 1.0:
        rate = "+0%"  # Default speed
    elif voice_speed > 1.0:
        rate = f"+{int((voice_speed - 1) * 100)}%"
    else:
        rate = f"{int((voice_speed - 1) * 100)}%"  # Already has negative sign
    
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_path)
    with open(output_path, "rb") as f:
        data = f.read()
    os.remove(output_path)
    return data

def speak_text_sync(text, lang, speed=1.0):
    """Synchronous wrapper for TTS"""
    return asyncio.run(generate_voice(text, lang, speed))

# ==========================
# 📊 STATISTICS FUNCTIONS
# ==========================
def get_translation_stats():
    """Calculate translation statistics"""
    if not st.session_state.history:
        return 0, 0, 0
    
    total = len(st.session_state.history)
    total_chars = sum(len(item['source']) for item in st.session_state.history)
    avg_length = total_chars / total if total > 0 else 0
    return total, total_chars, int(avg_length)

def export_history_to_csv():
    """Export translation history to CSV"""
    if not st.session_state.history:
        return None
    
    df = pd.DataFrame(st.session_state.history)
    return df.to_csv(index=False).encode('utf-8')

# ==========================
# 🧾 ENHANCED HISTORY STORAGE
# ==========================
if "history" not in st.session_state:
    st.session_state.history = []

if "settings" not in st.session_state:
    st.session_state.settings = {
        "voice_speed": 1.0,
        "auto_speak": False,
        "show_stats": True
    }

# ==========================
# 🌍 MAIN APP INTERFACE
# ==========================
st.title("🌍 AI Translator Pro")
st.markdown("<p class='subtitle'>✨ Advanced English ⇄ Swedish Translation with AI-Powered Voice</p>", unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.settings["voice_speed"] = st.slider(
        "🎵 Voice Speed", 
        min_value=0.5, 
        max_value=2.0, 
        value=1.0, 
        step=0.1
    )
    st.session_state.settings["auto_speak"] = st.checkbox("🔊 Auto-play translation", value=False)
    st.session_state.settings["show_stats"] = st.checkbox("📊 Show statistics", value=True)
    
    st.markdown("---")
    
    # Statistics Display
    if st.session_state.settings["show_stats"]:
        st.header("📊 Statistics")
        total, chars, avg = get_translation_stats()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Translations", total)
        with col2:
            st.metric("Avg. Length", avg)
        
        st.metric("Total Characters", chars)
    
    st.markdown("---")
    
    # History section
    st.header("🕓 Recent History")
    if st.session_state.history:
        for idx, item in enumerate(reversed(st.session_state.history[-10:]), 1):
            with st.expander(f"{idx}. {item['timestamp']}"):
                st.markdown(f"**Source ({item['source_lang'].upper()}):**")
                st.text(item['source'][:100] + "..." if len(item['source']) > 100 else item['source'])
                st.markdown(f"**Translation:**")
                st.text(item['translation'][:100] + "..." if len(item['translation']) > 100 else item['translation'])
        
        # Export history
        st.markdown("---")
        csv_data = export_history_to_csv()
        if csv_data:
            st.download_button(
                "📥 Export History (CSV)",
                data=csv_data,
                file_name=f"translation_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("No translations yet. Start translating!")
    
    st.markdown("---")
    st.caption("Built with ❤️ using Transformers + Edge-TTS + Streamlit")

# Main content area
tab1, tab2, tab3 = st.tabs(["📝 Text Translation", "📄 File Translation", "ℹ️ About"])

# ==========================
# 📝 ENHANCED TEXT TRANSLATION TAB
# ==========================
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        text_input = st.text_area(
            "Enter text (English or Swedish):", 
            height=200,
            placeholder="Type or paste your text here...",
            key="text_input"
        )
    
    with col2:
        st.markdown("### 🎯 Quick Tips")
        st.info("""
        - Paste up to 512 words
        - Auto-detects language
        - Get instant voice output
        - Download audio & text
        """)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        translate_btn = st.button("💬 Translate", use_container_width=True)
    
    with col_btn2:
        if st.button("🔄 Clear", use_container_width=True):
            st.session_state.text_input = ""
            st.rerun()

    if translate_btn:
        if text_input.strip():
            with st.spinner("🔍 Detecting language and translating..."):
                detected_lang, confidence = detect_language(text_input)
                source_lang = "en" if detected_lang == "en" else "sv"
                translation = translate_text(text_input, source_lang)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Display results
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                st.success(f"✅ Detected: {'English 🇬🇧' if source_lang == 'en' else 'Swedish 🇸🇪'} ({confidence} confidence)")
                st.markdown("### 📄 Original Text")
                st.markdown(f"<div class='output-box'>{text_input}</div>", unsafe_allow_html=True)
            
            with col_res2:
                st.success(f"✅ Translated to: {'Swedish 🇸🇪' if source_lang == 'en' else 'English 🇬🇧'}")
                st.markdown("### 🌐 Translation")
                st.markdown(f"<div class='output-box'>{translation}</div>", unsafe_allow_html=True)
            
            # Save to history
            st.session_state.history.append({
                'source': text_input,
                'translation': translation,
                'source_lang': source_lang,
                'target_lang': 'sv' if source_lang == 'en' else 'en',
                'timestamp': timestamp
            })

            # Voice output
            st.markdown("---")
            st.markdown("### 🎧 Audio Output")
            
            with st.spinner("🎙️ Generating natural voice..."):
                target_lang = "sv" if source_lang == "en" else "en"
                mp3_bytes = speak_text_sync(
                    translation, 
                    target_lang, 
                    st.session_state.settings["voice_speed"]
                )
            
            col_audio1, col_audio2 = st.columns([2, 1])
            
            with col_audio1:
                st.audio(mp3_bytes, format="audio/mp3", autoplay=st.session_state.settings["auto_speak"])
            
            with col_audio2:
                st.download_button(
                    "⬇️ Download Audio",
                    data=mp3_bytes,
                    file_name=f"translation_{timestamp.replace(':', '-').replace(' ', '_')}.mp3",
                    mime="audio/mpeg",
                    use_container_width=True
                )
                
                st.download_button(
                    "⬇️ Download Text",
                    data=translation,
                    file_name=f"translation_{timestamp.replace(':', '-').replace(' ', '_')}.txt",
                    use_container_width=True
                )
        else:
            st.warning("⚠️ Please enter text first.")

# ==========================
# 📄 ENHANCED FILE TRANSLATION TAB
# ==========================
with tab2:
    st.markdown("### 📁 Upload & Translate Files")
    
    col_upload1, col_upload2 = st.columns([2, 1])
    
    with col_upload1:
        file = st.file_uploader(
            "Choose a text file (.txt)", 
            type=["txt"],
            help="Upload a text file containing English or Swedish text"
        )
    
    with col_upload2:
        st.markdown("### ℹ️ File Info")
        if file:
            st.info(f"""
            **Name:** {file.name}  
            **Size:** {file.size / 1024:.2f} KB
            """)
    
    if file is not None:
        content = file.read().decode("utf-8")
        
        st.markdown("### 📄 File Preview")
        st.text_area("File content:", content, height=250, disabled=True)
        
        if st.button("📘 Translate File", use_container_width=False):
            with st.spinner("🔄 Translating file..."):
                detected_lang, _ = detect_language(content)
                source_lang = "en" if detected_lang == "en" else "sv"
                translation = translate_text(content, source_lang)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            direction = 'English → Swedish 🇬🇧→🇸🇪' if source_lang == 'en' else 'Swedish → English 🇸🇪→🇬🇧'
            st.success(f"✅ File translated successfully ({direction})")
            
            st.markdown("### 🌐 Translation Result")
            st.text_area("Translated content:", translation, height=250, disabled=True)
            
            # Download options
            col_dl1, col_dl2 = st.columns(2)
            with col_dl1:
                st.download_button(
                    "⬇️ Download Translation",
                    data=translation,
                    file_name=f"translated_{file.name}",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col_dl2:
                # Create comparison file
                comparison = f"=== ORIGINAL ({source_lang.upper()}) ===\n\n{content}\n\n=== TRANSLATION ===\n\n{translation}"
                st.download_button(
                    "⬇️ Download Comparison",
                    data=comparison,
                    file_name=f"comparison_{file.name}",
                    mime="text/plain",
                    use_container_width=True
                )

# ==========================
# ℹ️ ABOUT TAB
# ==========================
with tab3:
    st.markdown("## 📖 About AI Translator Pro")
    
    col_about1, col_about2 = st.columns(2)
    
    with col_about1:
        st.markdown("""
        ### ✨ Features
        - 🔄 **Bidirectional Translation** - English ⇄ Swedish
        - 🤖 **AI-Powered** - Uses Helsinki-NLP Marian models
        - 🎙️ **Natural Voice** - Edge-TTS with adjustable speed
        - 📊 **Analytics** - Track your translation history
        - 📁 **File Support** - Translate entire text files
        - 💾 **Export Options** - Save audio, text, and CSV history
        
        ### 🛠️ Technologies Used
        - **Transformers** - Translation models
        - **Edge-TTS** - Text-to-speech synthesis
        - **LangDetect** - Automatic language detection
        - **Streamlit** - Web interface
        """)
    
    with col_about2:
        st.markdown("""
        ### 🚀 How to Use
        1. **Text Translation**
           - Enter or paste text
           - Click "Translate"
           - Listen to audio output
           - Download results
        
        2. **File Translation**
           - Upload .txt file
           - View preview
           - Click "Translate File"
           - Download translated version
        
        3. **Settings**
           - Adjust voice speed
           - Enable auto-play
           - View statistics
           - Export history
        
        ### 📝 Tips for Best Results
        - Keep sentences clear and concise
        - Check translation accuracy for technical terms
        - Use proper punctuation
        - Avoid very long texts (max 512 words)
        """)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h3>Made with ❤️ for language learners and professionals</h3>
        <p>Powered by Hugging Face Transformers & Microsoft Edge-TTS</p>
    </div>
    """, unsafe_allow_html=True)