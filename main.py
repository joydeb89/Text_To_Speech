import streamlit as st
import requests
import os
from dotenv import load_dotenv
from gtts import gTTS  # Import gTTS for text-to-speech functionality
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

# Set page configuration
st.set_page_config(page_title="বাংলা টেক্সট টু স্পিচ", page_icon="🎙️")
st.title("🎙️ বাংলা টেক্সট টু স্পিচ")
st.write("আপনার বাংলা টেক্সট লিখুন এবং শুনুন বা ডাউনলোড করুন।")

# Input text for TTS
text = st.text_area("বাংলা টেক্সট", placeholder="এখানে বাংলা লিখুন...", height=150)

# Fetch Generation Info button
if st.button("🎤 প্রজন্ম তথ্য দেখুন"):
    api_key = os.getenv("X_API_KEY")  # Get API key from environment variable
    if not api_key:
        st.error("API কী খুঁজে পাওয়া যায়নি। .env ফাইলে X_API_KEY সেট করুন।")
    else:
        try:
            # API URL and headers
            url = "https://prod-api2.desivocal.com/dv/api/v0/tts_api/generation_info"
            headers = {"X_API_KEY": api_key}

            # Make GET request to DesiVocal API
            response = requests.get(url, headers=headers)

            # Check for a successful response
            if response.status_code == 200:
                # Display response text in Streamlit
                st.success("✅ প্রজন্ম তথ্য পাওয়া গেছে:")
                st.code(response.text)
            else:
                st.error(f"⚠️ API অনুরোধ ব্যর্থ হয়েছে। Status: {response.status_code}")
                st.text(response.text)
        except Exception as e:
            st.error(f"অনুরোধ ব্যর্থ হয়েছে: {e}")

# Text-to-Speech functionality (same as previous code)
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🎧 শোনান"):
        if not text.strip():
            st.warning("অনুগ্রহ করে কিছু টেক্সট লিখুন।")
        else:
            with st.spinner("অডিও তৈরি হচ্ছে..."):
                try:
                    tts = gTTS(text=text, lang='bn')
                    mp3_fp = BytesIO()
                    tts.write_to_fp(mp3_fp)
                    mp3_fp.seek(0)

                    st.audio(mp3_fp, format="audio/mp3")

                    st.download_button(
                        label="⬇️ ডাউনলোড করুন",
                        data=mp3_fp,
                        file_name="bengali_speech.mp3",
                        mime="audio/mp3"
                    )
                except Exception as e:
                    st.error(f"ত্রুটি: {e}")
