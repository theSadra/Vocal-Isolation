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

def separate_song(path):
    """Run Demucs to separate audio stems"""
    print(f"\n🎧 Processing: {path}")
    
    try:
        subprocess.run(["demucs", "--mp3", path], cwd=OUTPUT, check=True)
        print("✅ Separation complete")
    except subprocess.CalledProcessError as e:
        print(f"❗ Separation failed: {e}")
        raise

    base = os.path.splitext(os.path.basename(path))[0]
    model = os.path.join(SEPARATED, "htdemucs", base)
    
    # Load stems
    vocals = AudioSegment.from_file(os.path.join(model, "vocals.mp3"))
    drums = AudioSegment.from_file(os.path.join(model, "drums.mp3")) 
    bass = AudioSegment.from_file(os.path.join(model, "bass.mp3"))
    other = AudioSegment.from_file(os.path.join(model, "other.mp3"))
    
    # Combine instrumental
    instrumental = drums.overlay(bass).overlay(other)
    print("✅ Stems processed")


print("🎵 Select one or more songs to process.")
files = choose_audio_files()

if not files:
    print("❌ No files selected.")
else:
    for path in files:
        try:
            separate_song(path)
        except Exception:
            print(f"Skipping {path} due to errors")