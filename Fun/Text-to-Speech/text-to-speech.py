import os
from gtts import gTTS
import docx
from tkinter import Tk, filedialog

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def text_to_speech(text, output_file="transcript_audio.mp3"):
    tts = gTTS(text, lang="en")
    tts.save(output_file)
    print(f"Audio saved as {output_file}")

def main():
    # Open file dialog to select the Word document
    Tk().withdraw()  # Hide the root Tk window
    file_path = filedialog.askopenfilename(title="Select a Word Document", filetypes=[("Word Documents", "*.docx")])
    
    if not file_path:
        print("No file selected.")
        return
    
    try:
        text = extract_text_from_docx(file_path)
        if text.strip():
            text_to_speech(text)
        else:
            print("The document is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
