from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import librosa
from tensorflow.keras.models import load_model
from io import BytesIO


app = FastAPI()

origins = [
    "http://localhost:5173",  # your frontend
    "http://127.0.0.1:5173",  # sometimes used
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model("tone_lstm_model.h5")

def preprocess_audio(y, sr, n_steps=50):
    f0, voiced_flag, voiced_probs = librosa.pyin(y, 
                                                     sr=sr,
                                                     fmin=75,
                                                     fmax=500)
    f0 = np.nan_to_num(f0)
    nonzero_idx = np.where(f0 != 0)[0]

    if len(nonzero_idx) == 0:
        return None

    f0_non_silent = f0[nonzero_idx[0]:nonzero_idx[-1] + 1]
    f0_non_silent = (f0_non_silent - np.mean(f0_non_silent)) / (np.std(f0_non_silent) + 1e-6)




    f0_interp = np.interp(
        np.linspace(0, len(f0_non_silent)-1, n_steps),
        np.arange(len(f0_non_silent)), 
        f0_non_silent
    )

    return f0_interp.reshape(1, n_steps, 1)
    
    
# Route to predict tone from user's audio
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await(file.read())
    audio_file = BytesIO(contents)
    
    y, sr = librosa.load(audio_file, sr=22050)
    X_input = preprocess_audio(y, sr)
    if X_input is None:
        return {"tone": None, "probabilities": None, "message": "Silence detected"}
    
    probabilities = model.predict(X_input)
    pred_tone = int(np.argmax(probabilities, axis=1)[0] + 1)

    return {"tone": pred_tone, "probabilities": probabilities.tolist()}

