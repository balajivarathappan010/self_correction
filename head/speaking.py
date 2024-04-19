import subprocess
import pygame
import io
import pyttsx3

def speak(text):
    voice = "en-US-AriaNeural"
    command = f'edge-tts --voice "{voice}" --text "{text}" --rate=+30%'
    
    try:
        audio_data = subprocess.check_output(command, shell=True)
        pygame.init()
        pygame.mixer.init()
        audio_buffer = io.BytesIO(audio_data)
        pygame.mixer.music.load(audio_buffer)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(e)
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()