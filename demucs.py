import os
import subprocess
import shutil
from pydub import AudioSegment
from tkinter import Tk, filedialog

# Constants
OUTPUT = os.path.dirname(os.path.abspath(__file__))
SEPARATED = os.path.join(OUTPUT, "separated")

def choose_audio_files():
    """Open file dialog to select audio files"""
    Tk().withdraw()
    return filedialog.askopenfilenames(
        title="Select MP3 or WAV files",
        filetypes=[("Audio Files", "*.mp3 *.wav")]
    )

print("🎵 Select one or more songs to process.")
files = choose_audio_files()

if not files:
    print("❌ No files selected.")
else:
    print(f"Selected {len(files)} files for processing")