# Webcam Usage Detector with Audio and Notifications

This Python tool monitors Windows registry keys to detect which applications are currently using the webcam. When webcam usage is detected, it plays a custom alert sound, announces the PID of the application via text-to-speech (TTS), and triggers a Windows notification showing the process ID and executable name.

## Features

- Detects active webcam users by reading Windows registry keys.
- Plays an alert sound downloaded dynamically to a temporary folder.
- Announces the PID of the process accessing the webcam via TTS.
- Shows a Windows toast notification with the process ID and executable name.
- Automatically cleans up temporary files on exit.

## Requirements

- Windows OS (tested on Windows 10/11)
- Python 3.7 or newer

### Python Dependencies

- Install required Python packages via pip:

pip install -r requirements.txt

- Or individually:

pip install pygame pyttsx3 psutil win10toast

#### Usage

- Clone this repository or download the files.
- Run the script:

python main.py

- The script will monitor webcam usage continuously and print apps using the webcam with their PIDs.
- When a new webcam user is detected, it will:
- Play the alert audio.
- Announce the PID using TTS.
- Show a Windows notification with the PID and executable name.
- To exit, press Ctrl+C.

