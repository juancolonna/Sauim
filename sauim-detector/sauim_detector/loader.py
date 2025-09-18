import librosa
from scipy import signal
import numpy as np

def normalizar_amplitude(y: np.ndarray):
    peak = np.max(np.abs(y))
    if peak > 0:
        y = y / peak
    return y

def load_audio(filepath, sr=None):
    """
    Carrega um arquivo de áudio usando librosa.
    
    Args:
        filepath (str): caminho para o arquivo .wav
        sr (int ou None): taxa de amostragem alvo. 
                          Se None, mantém a original.
    Returns:
        y (np.ndarray): waveform
        sr (int): taxa de amostragem
    """
    y, sr = librosa.load(filepath, sr=sr, mono=True)
    y = normalizar_amplitude(y)
    # 2) Design a band-pass Butterworth (4th order). Nyquist = fs/2, SciPy handles normalization with fs=
    sos = signal.butter(N=4, Wn=[5000.0, 10000.0], btype="bandpass", fs=32000, output="sos")
    # 3) Zero-phase filtering (filtfilt) along the time axis (axis=0 for (samples, channels))
    y = signal.sosfiltfilt(sos, y, axis=0)
    return y, sr
