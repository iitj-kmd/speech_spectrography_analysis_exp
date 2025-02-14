import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# 1. Load audio
y, sr = librosa.load('sample-audio-2.wav')  # y: audio time series, sr: sampling rate

# 2. Compute the Mel spectrogram
mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128) # Adjust n_mels

# 3. Convert to log scale (dB)
log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

# 4. Display the Mel spectrogram
librosa.display.specshow(log_mel_spectrogram, sr=sr, x_axis='time', y_axis='mel')
plt.colorbar(format='%+2.0f dB')
plt.title('Mel spectrogram')
plt.tight_layout()
plt.show()