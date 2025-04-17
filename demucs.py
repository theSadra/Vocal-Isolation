import os
import subprocess
import shutil
from pydub import AudioSegment
from tkinter import Tk, filedialog

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
    
    subprocess.run(["demucs", "--mp3", path], cwd=OUTPUT, check=True)

    base = os.path.splitext(os.path.basename(path))[0]
    model = os.path.join(SEPARATED, "htdemucs", base)

    # Load stems
    vocals = AudioSegment.from_file(os.path.join(model, "vocals.mp3"))
    drums = AudioSegment.from_file(os.path.join(model, "drums.mp3"))
    bass = AudioSegment.from_file(os.path.join(model, "bass.mp3"))
    other = AudioSegment.from_file(os.path.join(model, "other.mp3"))

    # Combine instrumental
    instrumental = drums.overlay(bass).overlay(other)

    # Save clean output to: separated/{song_name}/
    folder = os.path.join(OUTPUT, base)
    os.makedirs(folder, exist_ok=True)
    vocals.export(os.path.join(folder, "vocals.mp3"), format="mp3")
    instrumental.export(os.path.join(folder, "instrumental.mp3"), format="mp3")

    # Clean up the intermediate Demucs folder
    shutil.rmtree(os.path.join(SEPARATED, "htdemucs"))
    print(f"✅ Saved: {folder}")

try:
    print("🎵 Select one or more songs to process.")
    files = choose_audio_files()

    if not files:
        print("❌ No files selected.")
    else:
        for path in files:
            separate_song(path)

        print(f"\n🎉 Done! Check the 'separated' folder at:\n{SEPARATED}")

except Exception as e:
    print(f"❗ Error: {e}")