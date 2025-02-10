from googletrans import Translator

# Supported languages mapping (Google Translate codes)
LANGUAGE_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Tamil": "ta",
    "Telugu": "te",
}

def translate_text(text, target_language):
   
    translator = Translator()
    lang_code = LANGUAGE_CODES.get(target_language, "en")  
    try:
        translated = translator.translate(text, dest=lang_code)
        return translated.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text  
