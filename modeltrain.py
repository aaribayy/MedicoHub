import pandas as pd
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

# Load the dataset
dataset = pd.read_csv('datasets/Training.csv')

# Preprocess the data
X = dataset.drop('prognosis', axis=1)
y = dataset['prognosis']
le = LabelEncoder()
le.fit(y)
Y = le.transform(y)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=20)

# Train the model
svc = SVC(kernel='linear')
svc.fit(X_train, y_train)

# Save the model
with open('svc.pkl', 'wb') as model_file:
    pickle.dump(svc, model_file)

print("Model trained and saved as svc.pkl")
