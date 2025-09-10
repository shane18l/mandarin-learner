from tensorflow.keras.models import load_model
import sounddevice as sd
import librosa
import numpy as np
import os
import soundfile as sf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

model = load_model("tone_lstm_model.h5")

duration = 2 
sr = 22050
print("Speak now")

y = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='float32')
sd.wait()
y = y.flatten()

# Save audio files, with predictions


f0, voiced_flag, voiced_probs = librosa.pyin(y, 
                                                    sr=sr,
                                                    fmin=75,
                                                    fmax=500)
f0 = np.nan_to_num(f0)
nonzero_idx = np.where(f0 != 0)[0]

if len(nonzero_idx) == 0:
    print("silence")

f0_non_silent = f0[nonzero_idx[0]:nonzero_idx[-1] + 1]
f0_non_silent = (f0_non_silent - np.mean(f0_non_silent)) / (np.std(f0_non_silent) + 1e-6)




f0_interp = np.interp(
    np.linspace(0, len(f0_non_silent)-1, 50),
    np.arange(len(f0_non_silent)), 
    f0_non_silent
)

X_input = f0_interp.reshape(1, len(f0_interp), 1)

predict_probabilities = model.predict(X_input)
print(predict_probabilities)
pred_tone = np.argmax(predict_probabilities, axis=1)[0] + 1
print(pred_tone)
    
filename = f"recording_pred{pred_tone}.wav"
sf.write(filename, y, sr)
    

   

