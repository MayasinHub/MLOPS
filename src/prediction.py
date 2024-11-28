# Prediction

# Import Libraries
import os
import pickle
import joblib
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
from google.colab import files
from scipy.stats import ks_2samp
from matplotlib import pyplot as plt
from tensorflow.keras.regularizers import l2
from tensorflow.keras.models import Sequential
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from tensorflow.keras import layers, models, regularizers
from sklearn.metrics import confusion_matrix, accuracy_score
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

#Connect to Google Drive
from google.colab import drive
drive.mount('/content/drive')

#Load the dataset
student_data = '/content/drive/My Drive/student-data.csv'
df = pd.read_csv(student_data)

# Features and labels of the model
X = df.drop(['Target'], axis=1)
y = df['Target']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)


scaler = StandardScaler()

# Fit the scaler on the training features and transform both train and test features
X_train_standardized = scaler.fit_transform(X_train)
X_test_standardized = scaler.transform(X_test)

# Convert back to DataFrame for easier saving and handling
X_train_standardized = pd.DataFrame(
    X_train_standardized, columns=X_train.columns)
X_test_standardized = pd.DataFrame(X_test_standardized, columns=X_test.columns)

# Initialize the RandomForestClassifier
model = RandomForestClassifier()

# Fit the model to the training data
model.fit(X_train_standardized, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test_standardized)

# Calculate precision, recall, and F1-score
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

# Print evaluation metrics
print(f"Model Evaluation Metrics")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")
print(f"Accuracy: {accuracy:.4f}")

# Create the confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Print the confusion matrix
print("Confusion Matrix:")
print(conf_matrix)

# Visualize the confusion matrix using a heatmap
plt.figure(figsize=(12, 6))
class_labels = ['Dropout', 'Graduated', 'Enrolled']
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Reds', xticklabels=class_labels, yticklabels=class_labels)
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()


# Create the directory if it does not exist
os.makedirs('./model', exist_ok=True)

# Save and download the model in the pickle file in the Saved Models folder
pickle.dump(model, open('./model/student-predictor.pkl', 'wb'))
files.download('./model/student-predictor.pkl')
