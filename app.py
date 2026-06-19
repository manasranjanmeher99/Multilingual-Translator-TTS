import streamlit as st
from mtranslate import translate
import pandas as pd
import os
from gtts import gTTS
import base64

# ---------------------------
# PAGE CONFIGURATION
# ---------------------------
st.set_page_config(
    page_title="Multilingual Translator",
    page_icon="🌐",
    layout="wide"
)

# ---------------------------
# CUSTOM CSS
# ---------------------------
st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

h1 {
    color: #4CAF50;
    font-weight: bold;
}

.stTextArea textarea {
    font-size: 18px;
}

.stButton button,
.stDownloadButton button {
    width: 100%;
    border-radius: 10px;
}

[data-testid="metric-container"] {
    border: 1px solid rgba(28,131,225,0.2);
    padding: 10px;
    border-radius: 10px;
}

.footer {
    text-align: center;
    color: gray;
    padding-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------
st.markdown("""
# 🌐 Multilingual Translator & Text-to-Speech

Translate text into multiple languages and listen to the pronunciation.
""")

st.divider()

# ---------------------------
# LOAD LANGUAGE DATASET
# ---------------------------
df = pd.read_csv("language.csv")

df.dropna(inplace=True)

lang = df['name'].to_list()
langcode = df['iso'].to_list()

langlist = sorted(lang)

# Language Dictionary
lang_array = {
    lang[i]: langcode[i]
    for i in range(len(langcode))
}

if "history" not in st.session_state:
    st.session_state.history = []


# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.header("⚙️ Translation Settings")

choice = st.sidebar.selectbox(
    "🔍 Search and Select Language",
    langlist
)
st.sidebar.markdown("---")
st.sidebar.subheader("📜 Translation History")

if st.sidebar.button("Show History"):
    if st.session_state.history:
        st.sidebar.dataframe(
            pd.DataFrame(st.session_state.history)
        )
    else:
        st.sidebar.info("No history available.")

if st.sidebar.button("Clear History"):
    st.session_state.history = []
    st.sidebar.success("History Cleared!")

# ---------------------------
# SPEECH SUPPORTED LANGUAGES
# ---------------------------
speech_langs = {
    "af": "Afrikaans",
    "ar": "Arabic",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
    "gu": "Gujarati",
    "or": "Odia",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "hy": "Armenian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it": "Italian",
    "ja": "Japanese",
    "jw": "Javanese",
    "km": "Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    "la": "Latin",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mr": "Marathi",
    "my": "Myanmar",
    "ne": "Nepali",
    "nl": "Dutch",
    "no": "Norwegian",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "si": "Sinhala",
    "sk": "Slovak",
    "sq": "Albanian",
    "sr": "Serbian",
    "su": "Sundanese",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Filipino",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "zh-CN": "Chinese"
}


# ---------------------------
# AUDIO DOWNLOAD FUNCTION
# ---------------------------
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()

    bin_str = base64.b64encode(data).decode()

    href = f'''
    <a href="data:application/octet-stream;base64,{bin_str}"
    download="{os.path.basename(bin_file)}">
    📥 Download {file_label}
    </a>
    '''

    return href

# ---------------------------
# TEXT INPUT
# ---------------------------
inputtext = st.text_area(
    "✍️ Enter Text to Translate",
    height=150,
    placeholder="Type your text here..."
)

col1, col2 = st.columns(2)

with col1:
    st.metric("Characters", len(inputtext))

with col2:
    st.metric("Words", len(inputtext.split()))

# ---------------------------
# COLUMNS
# ---------------------------
c1, c2 = st.columns([4, 3])

# ---------------------------
# TRANSLATION
# ---------------------------
translate_btn = st.button("🚀 Translate")

if translate_btn and inputtext:



    try:
        output = translate(
            inputtext,
            lang_array[choice]
        )
        st.session_state.history.append({
            "Language": choice,
            "Input": inputtext,
            "Output": output
        })

        with c1:
            st.subheader("📝 Translated Text")

            st.text_area(
                "",
                output,
                height=220
            )
            st.download_button(
                label="📄 Download Translation",
                data=output,
                file_name="translated_text.txt",
                mime="text/plain"
            )

        # ---------------------------
        # TEXT TO SPEECH
        # ---------------------------
        selected_lang_code = lang_array[choice]

        with c2:

            st.subheader("🔊 Audio Output")

            # Odia not supported by gTTS
            if selected_lang_code == "or":

                st.info(
                    "🎤 Translation is available for Odia, but audio generation is not supported by gTTS."
                )

            else:

                audio_file = gTTS(
                    text=output,
                    lang=selected_lang_code,
                    slow=False
                )

                audio_file.save("lang.mp3")

                with open("lang.mp3", "rb") as f:
                    audio_bytes = f.read()

                st.audio(
                    audio_bytes,
                    format="audio/mp3"
                )

                st.markdown(
                    get_binary_file_downloader_html(
                        "lang.mp3",
                        "Audio File"
                    ),
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.error(f"Error: {e}")

# ---------------------------
# FOOTER
# ---------------------------
st.divider()

st.markdown(
    """
    <div class="footer">
        🌍 Built with Streamlit • mTranslate • gTTS | Created by Manas Ranjan Meher
    </div>
    """,
    unsafe_allow_html=True
)