import os
import subprocess
import streamlit as st
from pydub import AudioSegment
from io import BytesIO
import tempfile
import shutil

def separate_audio(uploaded):
    """Process the uploaded audio file and separate vocals/instrumental"""
    try:
        with st.spinner("Separating audio... (This may take a few minutes)"):
            # Create a properly named temporary file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as input:
                input.write(uploaded.getvalue())
                temp = input.name
            
            # Ensure the file is closed before processing
            del input

            # Run Demucs separation
            subprocess.run(["demucs", "--mp3", temp], check=True)
            
            # Load separated tracks
            base = os.path.splitext(os.path.basename(temp))[0]
            model = os.path.join("separated", "htdemucs", base)
            
            # Verify files exist before loading
            if not os.path.exists(model):
                raise FileNotFoundError(f"Demucs output not found at {model}")
            
            vocals = AudioSegment.from_file(os.path.join(model, "vocals.mp3"))
            drums = AudioSegment.from_file(os.path.join(model, "drums.mp3"))
            bass = AudioSegment.from_file(os.path.join(model, "bass.mp3"))
            other = AudioSegment.from_file(os.path.join(model, "other.mp3"))
            
            # Combine instrumental tracks
            instrumental = drums.overlay(bass).overlay(other)
            
            # Convert to bytes for Streamlit
            vocal_bytes = BytesIO()
            instrumental_bytes = BytesIO()
            
            vocals.export(vocal_bytes, format="mp3")
            instrumental.export(instrumental_bytes, format="mp3")
            
            # Clean up
            os.unlink(temp)
            shutil.rmtree("separated", ignore_errors=True)
            
            return vocal_bytes.getvalue(), instrumental_bytes.getvalue()
            
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
        # Clean up any remaining files
        if 'temp_path' in locals() and os.path.exists(temp):
            os.unlink(temp)
        shutil.rmtree("separated", ignore_errors=True)
        return None, None

st.title("🎵 Audio Separator")
st.markdown("Upload a song to separate vocals from instrumental")

uploaded = st.file_uploader(
    "Choose an MP3 or WAV file",
    type=["mp3", "wav"]
)

if uploaded is not None:
    st.audio(uploaded)
    
    if st.button("Separate Audio"):
        vocal_data, instrumental_data = separate_audio(uploaded)
        
        if vocal_data and instrumental_data:
            st.success("Separation complete!")
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.header("Vocals")
                st.audio(vocal_data, format="audio/mp3")
                st.download_button(
                    label="Download Vocals",
                    data=vocal_data,
                    file_name="vocals.mp3",
                    mime="audio/mp3"
                )
            
            with col2:
                st.header("Instrumental")
                st.audio(instrumental_data, format="audio/mp3")
                st.download_button(
                    label="Download Instrumental",
                    data=instrumental_data,
                    file_name="instrumental.mp3",
                    mime="audio/mp3"
                )