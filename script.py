import os
folder_name = 'tone_perfect'
import pandas as pd
import librosa
import matplotlib.pyplot as plt
import numpy as np
import re
csv_file_path = 'mandarin_tone_dataset2.csv'

# def add_to_csv():
#     directory = os.fsencode(folder_name)
#     for file in os.listdir(directory):
#         filename = os.fsdecode(file)
#         y, sr = librosa.load(filename)
#         f0, voiced_flag, voiced_probs = librosa.pyin(y, 
#                                                      sr=sr,
#                                                      fmin=75,
#                                                      fmax=500)
        
        
        # with open(csv_file_path, mode='w', newline='') as csv_file:
        #     writer = csv.writer(csv_file)
        #     writer.writerows


X = []
Y = []


def extract_f0(file_path):
    y, sr = librosa.load(f"tone_perfect/{file_path}")
    f0, voiced_flag, voiced_probs = librosa.pyin(y, 
                                                     sr=sr,
                                                     fmin=75,
                                                     fmax=500)
    f0 = np.nan_to_num(f0)

    f0_interp = np.interp(
        np.linspace(0, len(f0)-1, 50),
        np.arange(len(f0)),
        f0
    )
    
    

    mean_pitch = np.mean(f0)
    min_pitch = np.min(f0)
    max_pitch = np.max(f0)
    pitch_range = max_pitch - min_pitch
    slope = (f0[-1] - f0[0]) / len(f0)  # rough slope
    
    match = re.search(r'\d+', file_path)
    if match: 
        tone_num = int(match.group())
    else:
        tone_num = 0
        
    features = [mean_pitch, min_pitch, max_pitch, pitch_range, slope]

    X.append(features)
    Y.append(tone_num)
    print(f"{file_path}: {features}\n {tone_num}")

directory = os.fsencode(folder_name)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    extract_f0(filename)
    
df = pd.DataFrame(X, columns=["mean_pitch", "min_pitch", "max_pitch", "pitch_range", "slope"])
df["tone"] = Y
df.to_csv(csv_file_path, index=False)

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))