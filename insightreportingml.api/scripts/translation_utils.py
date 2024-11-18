import time
from deep_translator import GoogleTranslator
from deep_translator.exceptions import TooManyRequests
from transformers import pipeline

def translate_to_english(text, language_code): 
    max_chars_per_request = 500
    translated_text = []

    chunks = [text[i:i + max_chars_per_request] for i in range(0, len(text), max_chars_per_request)]

    for chunk in chunks:
        try:
            translated_chunk = GoogleTranslator(source=language_code, target='en').translate(chunk)
            translated_text.append(translated_chunk)
            time.sleep(0.3)
        
        except TooManyRequests:
            print("Too many requests to the Google translation server. Switching to Hugging Face fallback translation.")
            translator = pipeline("translation", model=f"Helsinki-NLP/opus-mt-{language_code}-en")
            return fallback_translation(chunks, translator)

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    return ' '.join(translated_text)

def fallback_translation(chunks, translator):
    translated_text = []
    
    for chunk in chunks:
        translated_chunk = translator(chunk, max_length=512)[0]['translation_text']
        translated_text.append(translated_chunk)

    return ' '.join(translated_text)