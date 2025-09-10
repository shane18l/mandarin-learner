from tensorflow.keras.models import load_model
model = load_model('/content/drive/MyDrive')

def extract_f0(file_path):
    y, sr = librosa.load(f"tone_perfect/{file_path}")
    f0, voiced_flag, voiced_probs = librosa.pyin(y, 
                                                     sr=sr,
                                                     fmin=75,
                                                     fmax=500)
    f0 = np.nan_to_num(f0)
    nonzero_idx = np.where(f0 != 0)[0]

    if len(nonzero_idx) == 0:
        return 

    f0_non_silent = f0[nonzero_idx[0]:nonzero_idx[-1] + 1]
    f0_non_silent = (f0_non_silent - np.mean(f0_non_silent)) / (np.std(f0_non_silent) + 1e-6)




    f0_interp = np.interp(
        np.linspace(0, len(f0_non_silent)-1, 50),
        np.arange(len(f0_non_silent)), 
        f0_non_silent
    )
    
    

   
    match = re.search(r'\d+', file_path)
    if match: 
        tone_num = int(match.group())
    else:
        tone_num = 0


    X.append(f0_interp)
    Y.append(tone_num)