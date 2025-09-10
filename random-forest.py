import pandas as pd

df = pd.read_csv('mandarin_tone_dataset.csv')
feature_cols = ["mean_pitch", "min_pitch", "max_pitch", "pitch_range", "slope"]
df = df[(df[feature_cols] != 0).any(axis=1)]

print(df.shape)

X = df[feature_cols].values
y = df["tone"].values

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