import threading
import tkinter as tk
from tkinter import messagebox
import numpy as np
import sounddevice as sd

# Audio config
SAMPLE_RATE = 44100
DURATION = 2.0  # in seconds
THRESHOLD = 0.02  # Amplitude threshold for voice detection

class VoiceDetector:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Detector")
        self.root.geometry("300x200")
        self.detecting = False

        self.status_label = tk.Label(root, text="Status: Idle", font=("Arial", 14))
        self.status_label.pack(pady=20)

        self.toggle_button = tk.Button(root, text="Start Detection", command=self.toggle_detection)
        self.toggle_button.pack(pady=10)

    def toggle_detection(self):
        if self.detecting:
            self.detecting = False
            self.toggle_button.config(text="Start Detection")
            self.status_label.config(text="Status: Idle", fg="black")
        else:
            self.detecting = True
            self.toggle_button.config(text="Stop Detection")
            self.status_label.config(text="Listening...", fg="blue")
            threading.Thread(target=self.detect_voice, daemon=True).start()

    def detect_voice(self):
        while self.detecting:
            audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float64')
            sd.wait()
            volume = np.linalg.norm(audio) / len(audio)

            if volume > THRESHOLD:
                self.status_label.config(text="Voice Detected!", fg="green")
            else:
                self.status_label.config(text="Listening...", fg="blue")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceDetector(root)
    root.mainloop()
