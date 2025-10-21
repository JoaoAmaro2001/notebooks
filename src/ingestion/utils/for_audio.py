from utils import *
import numpy as np
import pandas as pd
from IPython.display import Audio, display
from scipy.io.wavfile import write as wavwrite

def export_audio(dataset):

    import os 
    from utils import derivatives

    # Options
    fs = 44100  # if you know a different Fs for this recording, put it here
    ch = 1  # <- change if you want channel 0 or something else

    # ---- 1) Get raw mic data (handles numpy array or pandas object) ----
    raw = dataset.streams.Microphone.Audio.data  # shape (N,) or (N, C)

    # Choose a channel:
    # - If it's 1D, use as-is.
    # - If it's 2D, pick the channel you want (0-based). You used column 1 previously.
    if isinstance(raw, pd.DataFrame) or isinstance(raw, pd.Series):
        raw = raw.to_numpy()

    if raw.ndim == 1:
        mic_waveform = raw.astype(float)
    else:
        mic_waveform = raw[:, ch].astype(float)

    # ---- 2) Clean NaNs/Infs ----
    mic_waveform = np.nan_to_num(mic_waveform, nan=0.0, posinf=0.0, neginf=0.0)

    # ---- 3) Scale to a safe float range (-1..1) for playback ----
    # If original is integer-like, scale by its max possible magnitude; otherwise normalize by abs max.
    if np.issubdtype(mic_waveform.dtype, np.integer):
        max_abs = float(np.iinfo(mic_waveform.dtype).max)
    else:
        max_abs = float(np.max(np.abs(mic_waveform))) if np.max(np.abs(mic_waveform)) > 0 else 1.0

    audio_float = (mic_waveform / max_abs).astype(np.float32)

    wav_path = os.path.join(derivatives, "audio", "microphone_raw.wav")
    if not os.path.exists(wav_path):
        os.makedirs(wav_path)
        
    # scipy accepts float32 in [-1, 1] or int16; we already have float32 normalized
    wavwrite(wav_path, fs, audio_float)
    print(f"Saved: {wav_path}")
