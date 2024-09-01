import speech_recognition as sr

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_file) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source)
        
        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        raise Exception('Could not recognize audio')
    except sr.RequestError as e:
        raise Exception(f'API request error: {e}')
    except Exception as e:
        raise Exception(f'An unexpected error occurred: {e}')

def text_to_speech(audio):
    recognizer = sr.Recognizer()
    
    try:
        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        raise Exception('Could not recognize audio')
    except sr.RequestError as e:
        raise Exception(f'API request error: {e}')
    except Exception as e:
        raise Exception(f'An unexpected error occurred: {e}')
