import os
import subprocess
import shutil
from pydub import AudioSegment
from tkinter import Tk, filedialog

# Constants
OUTPUT = os.path.dirname(os.path.abspath(__file__))
SEPARATED = os.path.join(OUTPUT, "separated")

print("Audio Separation Tool - Initial Setup")