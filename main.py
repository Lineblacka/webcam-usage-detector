import time
import os
import urllib.request
import pygame
import tempfile
import atexit
import shutil
import pyttsx3
import psutil
from win10toast import ToastNotifier
from webcamDetect import WebcamDetect

# === Config ===
AUDIO_URL = "https://l.top4top.io/m_3437fp48c1.mp3"
temp_dir = tempfile.mkdtemp()
AUDIO_FILE = os.path.join(temp_dir, "alert.mp3")

# === Download sound ===
urllib.request.urlretrieve(AUDIO_URL, AUDIO_FILE)

# === Cleanup temp files on exit ===
def cleanup():
    try:
        shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"Cleanup error: {e}")

atexit.register(cleanup)

# === Init sound + TTS + notifications ===
pygame.mixer.init()
def play_sound():
    pygame.mixer.music.load(AUDIO_FILE)
    pygame.mixer.music.play()

engine = pyttsx3.init()
def speak_pid(pid):
    voices = engine.getProperty('voices')   
    engine.setProperty('voice', voices[1].id) 
    engine.say(f"{pid}")
    engine.runAndWait()

toaster = ToastNotifier()

def notify_webcam_on(pid):
    try:
        p = psutil.Process(pid)
        exe_name = os.path.basename(p.exe())
    except Exception:
        exe_name = "Unknown"
    message = f"Webcam turned on by process {pid}: {exe_name}"
    toaster.show_toast("Webcam Alert", message, duration=5, threaded=True)

webcamDetect = WebcamDetect()
webcam_active = False
spoken_pids = set()

try:
    while True:
        apps = webcamDetect.getActiveApps()
        if apps:
            for app_name, pids in apps:
                pid_str = str(pids[0]) if pids else "N/A"

            if not webcam_active:
                play_sound()
                # Notify and speak the first PID found
                first_pid = None
                for _, pids in apps:
                    if pids:
                        first_pid = pids[0]
                        break

                if first_pid and first_pid not in spoken_pids:
                    notify_webcam_on(first_pid)
                    time.sleep(3)
                    speak_pid(first_pid)
                    spoken_pids.add(first_pid)
                webcam_active = True
        else:
            webcam_active = False
        time.sleep(1)
except KeyboardInterrupt:
    exit()
