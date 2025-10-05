import streamlit as st
st.title('Transform any 🎵song🎵 in your voice! 🗣️')


section1 = st.container()
c1, c2, c3 = section1.columns([1,2,1])
c2.markdown("""
<h3 style="text-align:center">Saiyaara Title Track</h3>
<iframe 
  width="650" 
  height="380" 
  src="https://www.youtube-nocookie.com/embed/BSJa1UytM8w?si=eQEzrOGgLjr5zIvU&controls=1&start=60&autoplay=0&mute=1" 
  title="YouTube video player" 
  frameborder="0" 
  allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
  referrerpolicy="strict-origin-when-cross-origin" 
  allowfullscreen>
</iframe>
""", unsafe_allow_html=True)
c2.markdown('$$\Huge \overbrace{ \hspace{5cm} }$$')

section2 = st.container()
c1, c2 = section2.columns([1,1], gap='medium')
c1.markdown("""<h3 style="text-align:center">In the voice of <br>
<img src='https://paintwaint.in/cdn/shop/files/Untitled_38_7d6b8ce6-e96c-4496-8f31-24edf0570ade.png?crop=center&height=150&v=1712573448&width=150'></h3>""", 
unsafe_allow_html=True)
c1.audio('data/audiofiles/saiyaara_mudiji.mp3', format="audio/mp3",start_time=60)



c2.markdown("""<h3 style="text-align:center">In the voice of <br>
<img src='https://d3i6fh83elv35t.cloudfront.net/static/2018/05/GettyImages-961767096-1024x683.jpg' height=150></h3>
""", 
unsafe_allow_html=True)
c2.audio('data/audiofiles/saiyaara_trump2.mp3', format="audio/mp3", start_time=60)
c2.markdown("""<p style="text-align:center">for some reason I like this!!! ¯\_(ツ)_/¯ </p>""",unsafe_allow_html=True)

st.markdown('''
### Step by Step Process in Python for Google Colab or Kaggle Notebooks
1. Download a song from YouTube using `yt_dlp` python package
2. Split the audio into vocals and rest of the music using `demucs` a high quality source separation [library](https://github.com/facebookresearch/demucs) maintained by Meta
3. Download the refernce audio from Youtube or provide manually
4. Align the sample rates between source audio of the Song with Reference Audio of the Person using `librosa` and `soundfile`
5. Use [Seed-VC](https://github.com/Plachtaa/seed-vc) to transform the song into reference voice
6. Overlay the newly generated vocals with the rest of the song and save as mp3. 

#### Step 0: Preparing the Environment (Tricky)
Both Google Colab and Kaggle environments are setup with Pytoch 2.8.0, but seed-vc requirements are built for 2.4.0.
Here is a hacky fix
1. Clone the repository with `!git clone https://github.com/Plachtaa/seed-vc.git`
2. Install `munch` and `descript-audio-codec`. This will lead to an import error because of outdated `protobuf` library used by google creating dependency conflicts.
3. Install protobuf using `pip install -q protobuf==4.23.4 --force-reinstall`
4. Install the remaning libraries

```python
!git clone https://github.com/Plachtaa/seed-vc.git
!pip install -q munch
!pip install -q descript-audio-codec
!pip install -q pytube
!pip install -q yt_dlp
!pip install -q protobuf==4.23.4 --force-reinstall
!pip install -q demucs
```

#### Step 1: Split Audio
I just uploaded the mp3 I earlier downloaded and used `demucs` to separate.

```python
import demucs.separate

# Build the command arguments as list of strings
args = [
    "--two-stems=vocals",
    "-n", "htdemucs_ft",  # specifying model (optional)
    "--out", "separated_output",
    "/content/Saiyaara.mp3"
]

demucs.separate.main(args)
```

#### Step 2: Download reference audio

```python
import yt_dlp
import os
from IPython.display import display, Audio

def download_audio_with_ytdlp(url: str, start: str, end: str, output_template: str = "%(title)s.%(ext)s"):
    section_spec = f"*{start}-{end}"
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "postprocessor_args": [
                    "-ar", "44100"
                ],
        "download_sections": section_spec,
        "force_keyframes_at_cuts": True,
        "keepvideo": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info

ref_url = "https://www.youtube.com/shorts/RxZaKURW99M"
ref_out = os.path.join(downloads_path, 'ref.wav')
ref_metadata = download_audio_with_ytdlp(ref_url, start="0:00", end="0:15", output_template=ref_out)
```

#### Step 3: Trim relevant segment and align sampling rates
* Ideally keep segments that have variation in voice so that model has a reference of both higher and lower pitches
* The model takes in audio of 44100 Hz sample, so chose both refernce and source audio of this quality, otherwise sampling using librosa

```python
import numpy as np
import soundfile as sf
import librosa
def save_segment(audiopath, start, end):
    audio_name = os.path.join(downloads_path, f"{audiopath.split('/')[-1].split('.')[0]}_trim.wav")
    y, sr = librosa.load(audiopath)
    start_sample = int(np.floor(start * sr))
    end_sample = int(np.floor(end*sr))
    y = y[start_sample:end_sample]
    sf.write(audio_name, y, sr)
```
save_segment('/content/trump.mp3', 0, 20)

#### Step 4: Run Seed VC Diffusion
* Step into `seed-vc` cloned folder
* Save both source and reference files into the folder for seed-vc to acces
* Run inference like below
```bash
python inference.py 
--source saiyaara.wav 
--target trump.wav 
--output out_diff40 
--diffusion-steps 40 
--length-adjust 1.0 
--inference-cfg-rate 0.7 
--f0-condition True 
--semi-tone-shift 0 
--fp16 True
```

#### Step 5: Combine the output
Had to make the transformed vocal softer by using to `vocals_transformed-8` to merge better with the music
```python
from glob import glob
vocals_transformed = AudioSegment.from_file(glob('out_diff40/*')[0], format="wav")
novocals = AudioSegment.from_file('/content/seed-vc/separated_output/htdemucs_ft/Saiyaara/no_vocals.wav', format="wav")
overlay = (vocals_transformed-8).overlay(novocals, position=0)
overlay.export("saiyaara_trump.mp3", format="mp3")
```
and Voila !
''')
