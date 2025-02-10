from gtts import gTTS
import os

# Supported languages for gTTS (Google Text-to-Speech)
LANGUAGE_CODES_TTS = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Tamil": "ta",
    "Telugu": "te",
}

def text_to_speech(text, target_language):
    
    lang_code = LANGUAGE_CODES_TTS.get(target_language, "en")  
    
    try:
        tts = gTTS(text=text, lang=lang_code)
        audio_path = f"static/audio_{lang_code}.mp3"
        os.makedirs("static", exist_ok=True)
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        print(f"Speech synthesis error: {e}")
        return None  
