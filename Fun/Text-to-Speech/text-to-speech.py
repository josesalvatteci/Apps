import os
import docx
import streamlit as st
from gtts import gTTS

def extract_text_from_docx(file):
    """Extract text from an uploaded Word document."""
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def text_to_speech(text, output_file="transcript_audio.mp3"):
    """Convert text to speech and save as an audio file."""
    tts = gTTS(text, lang="en")
    tts.save(output_file)
    return output_file

# Streamlit UI
st.title("Word Document to Speech Converter")

# File uploader in Streamlit
uploaded_file = st.file_uploader("Upload a Word Document", type=["docx"])

if uploaded_file is not None:
    try:
        # Extract text
        text = extract_text_from_docx(uploaded_file)
        
        if text.strip():
            st.write("Extracted Text:")
            st.text_area("Text Content", text, height=250)

            # Convert text to speech
            audio_file = text_to_speech(text)

            # Provide a download link
            with open(audio_file, "rb") as file:
                st.download_button(label="Download Speech", data=file, file_name="transcript_audio.mp3", mime="audio/mp3")
        
        else:
            st.warning("The document is empty.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
