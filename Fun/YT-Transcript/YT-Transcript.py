import streamlit as st
import os
import re
from dotenv import load_dotenv
from groq import Groq
from youtube_transcript_api import YouTubeTranscriptApi

# Load API key securely
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("🚨 API Key is missing! Set it in Streamlit Secrets or a .env file.")
    st.stop()

# Streamlit UI Styling
st.set_page_config(page_title="YouTube AI Agent", page_icon="📺", layout="wide")

st.title("🎬 YouTube AI Agent: Video & Summary Generator")

# Input for YouTube Link
youtube_url = st.text_input("Enter YouTube Video URL", "https://www.youtube.com/watch?v=rN49URY3Q_c&t=3s")

# Extract video ID
def extract_video_id(url):
    pattern = r"(?:v=|/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None

# Get Transcript
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        return " ".join([entry["text"] for entry in transcript])
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

# Summarization Function
def summarize_text(text):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"""
    Summarize the following YouTube transcript:
    {text}
    Provide key insights in bullet points.
    """
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an AI assistant that summarizes YouTube transcripts."},
            {"role": "user", "content": prompt}
        ],
        model="llama3-8b-8192",
    )
    return response.choices[0].message.content

# Process Video if URL is provided
if youtube_url:
    video_id = extract_video_id(youtube_url)
    if video_id:
        st.video(youtube_url)
        transcript = get_transcript(video_id)
        if transcript:
            st.subheader("📜 Transcript Preview")
            st.write(transcript[:1000] + "..." if len(transcript) > 1000 else transcript)
            
            st.subheader("📝 AI-Generated Summary")
            summary = summarize_text(transcript)
            st.write(summary)
    else:
        st.error("Invalid YouTube URL. Please check and try again.")
