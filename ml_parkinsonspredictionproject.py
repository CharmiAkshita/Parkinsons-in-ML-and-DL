# -*- coding: utf-8 -*-
"""ML_ParkinsonsPredictionProject.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wJddaSJwNR8NvA_IxcygzuE8aULEEOW2

Importing necessary values
"""

# Commented out IPython magic to ensure Python compatibility.
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
sns.set()
import warnings
warnings.filterwarnings('ignore')

!pip install plotly
from plotly.offline import iplot
import plotly as py

# Get the current working directory
current_directory = os.getcwd()
print(f"Current working directory: {current_directory}")

"""Data collection and analysis"""

pd.set_option('display.max_rows', 195)
pd.set_option('display.max_columns', 24)
pd.set_option('display.width', 195)

df = pd.read_csv('/content/parkinsons.csv')
df

df.shape

#finding null value
df.isnull().sum()

df.dtypes

df['status'].value_counts()

df.info()

"""Distribution of dataset"""

# Iterate through numerical columns and create distribution plots
for column in df.select_dtypes(include='number'):
    sns.displot(df[column])  # Using displot instead of distplot (deprecated)
    plt.show()

#outlier

def boxplots(col):
  sns.boxplot(df[col])
  plt.show()

for i in list(df.columns)[1:]:
  boxplots(i)

"""Corelation matrix to find the relation between variables"""

#Dropping name column
if 'name' in df.columns:
  df=df.drop(columns=['name'])
#correlation
plt.figure(figsize=(20, 20))
sns.heatmap(df.select_dtypes(include=['number']).corr(), annot=True, cmap='rainbow')
plt.show()

"""Data Processing"""

X = df.drop(columns=['status'], axis=1)if 'status' in df.columns else df.copy() # Drop 'status' only if it's in the columns
Y = df['status']

X.head()

Y.head()

"""The dataset is not balanced here and there may be false +ve and false -ve values also.This is why instead of accuracy prceision and recall are considered."""

from imblearn.over_sampling import RandomOverSampler
from sklearn.preprocessing import MinMaxScaler
ros = RandomOverSampler()
X_ros, Y_ros = ros.fit_resample(X, Y)
print(Y.value_counts())
print("#############")
print(Y_ros.value_counts())

"""Feature Scaling"""

#Featuring scaling for optimized weight and optimized bias
from sklearn.preprocessing import MinMaxScaler

# Instantiate MinMaxScaler
scaler = MinMaxScaler((-1,1))

# Fit and transform the resampled data
X = scaler.fit_transform(X_ros)
Y = Y_ros

"""End of preprocessing"""

#checking the dataset
X.shape

"""Applying PCA(principle component analysis)"""

from sklearn.decomposition import PCA

pca = PCA(0.95)
X_pca = pca.fit_transform(X)
print(X.shape)
print(X_pca.shape)

pd.DataFrame(X_pca)

"""Train and test of data"""

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X_pca, Y, test_size=0.2, random_state=1)

"""Deep Learning"""

from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense
from keras import Sequential

model = Sequential()
model.add(Dense(32, activation='relu', input_dim = 22))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.summary()

def plot_history(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(acc) + 1)

    # Plot accuracy
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    plt.plot(epochs, acc, 'bo', label='Training accuracy')
    plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
    plt.title('Training and validation accuracy')
    plt.legend()

    # Plot loss
    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    plt.show()

model = Sequential()
model.add(Dense(32, activation='relu', input_dim=8)) # Change input_dim to 8 to match X_train's shape
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.summary()

model.compile(loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, Y_train, batch_size=32, epochs=200, validation_data=(X_test, Y_test))

"""Model Building"""

from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

list_met = []
list_accuracy = []

#Model 1
#logistic regression
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(C=0.4, max_iter=1000, solver='liblinear')
lr = classifier.fit(X_train, Y_train)
#prediction
Y_pred = classifier.predict(X_test)
#Accuracy
accuracy_LR = accuracy_score(Y_test, Y_pred)
accuracy_LR

#Model 2
from sklearn.tree import DecisionTreeClassifier
classifier2 = DecisionTreeClassifier(random_state=14)
dt = classifier2.fit(X_train, Y_train)
#prediction
Y_pred2 = classifier2.predict(X_test)
#Evaluation
accuracy_DT = accuracy_score(Y_test, Y_pred2)
accuracy_DT

#Model 3
#Through Gini - Linear measure
from sklearn.ensemble import RandomForestClassifier
classifier3 = RandomForestClassifier(random_state=14)
rfi = classifier3.fit(X_train, Y_train)
#prediction
Y_pred3 = classifier3.predict(X_test)
#Evaluation
accuracy_RFI = accuracy_score(Y_test, Y_pred3)
accuracy_RFI

#Model 4
#Through entropy - logarithmic measure
classifier4 = RandomForestClassifier(criterion = 'entropy', random_state=14)
rfe = classifier4.fit(X_train, Y_train)
#prediction
Y_pred4 = classifier4.predict(X_test)
#Evaluation
accuracy_RFE = accuracy_score(Y_test, Y_pred4)
accuracy_RFE

#Model 5
from sklearn.svm import SVC

model_svm = SVC()
SVM = model_svm.fit(X_train, Y_train)
#prediction
Y_pred5 = model_svm.predict(X_test)
#Evaluation
accuracy_SVC = accuracy_score(Y_test, Y_pred5)
accuracy_SVC

#Model 6
from sklearn.neighbors import KNeighborsClassifier
mode_knn = KNeighborsClassifier()
knn = mode_knn.fit(X_train, Y_train)
#prediction
pred_knn = mode_knn.predict(X_test)
#Evaluation
accuracy_knn = accuracy_score(Y_test, pred_knn)
accuracy_knn

#Model 7
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb = gnb.fit(X_train, Y_train)
#Prediction
pred_gnb = gnb.predict(X_test)
#Evaluation
accuracy_GNB = accuracy_score(Y_test, pred_gnb)
accuracy_GNB

#Model 8
from sklearn.naive_bayes import BernoulliNB
model = BernoulliNB()
bnb = model.fit(X_train, Y_train)
#Prediction
pred_bnb = bnb.predict(X_test)
#Evaluation
accuracy_BNB = accuracy_score(Y_test, pred_bnb)
accuracy_BNB

#Combining all the models by using voting classifier
from sklearn.ensemble import VotingClassifier
evc = VotingClassifier(estimators=[('lr', lr), ('DT', dt), ('RFI', rfi), ('RFE', rfe), ('SVC', SVM), ('KNN', knn), ('GNB', gnb), ('BNB', bnb)], voting= 'hard', flatten_transform = True)
model_evc = evc.fit(X_train, Y_train)
#Prediction
pred_evc = evc.predict(X_test)
#Evaluation
accuracy_evc = accuracy_score(Y_test, pred_evc)

list1 = ["logistic Regression","Decision Tree","Random Forest Gini","Random Forest Entropy","Support Vector","K Nearest Neighbors","GaussionNB","BernouliNB","Voting Classifier"]
list2 = [accuracy_LR,accuracy_DT,accuracy_RFI,accuracy_RFE,accuracy_SVC,accuracy_knn,accuracy_GNB,accuracy_BNB,accuracy_evc]
list3 = [classifier,classifier2,classifier3,classifier4,model_svm,mode_knn,gnb,model,model_evc]

df_accuracy = pd.DataFrame({'Method Used' : list1, 'Accuracy' : list2})
print(df_accuracy)

charts = sns.barplot(x = 'Method Used', y = 'Accuracy', data = df_accuracy)
charts.set_xticklabels(charts.get_xticklabels(), rotation=90)
print(charts)

from xgboost import XGBClassifier
model_xgb = XGBClassifier()
model_xgb.fit(X_train, Y_train)

Y_pred_xgb = model_xgb.predict(X_test)
print(accuracy_score(Y_test, Y_pred_xgb))

#other evaluation method
from sklearn.metrics import roc_curve, auc

#randomForest entropy
Y_pred4_train= classifier4.predict(X_train)
Y_pred4_test= classifier4.predict(X_test)

#KNN
from sklearn.neighbors import KNeighborsClassifier #Import the KNeighborsClassifier
model_knn = KNeighborsClassifier() #Initialize the model
model_knn = model_knn.fit(X_train, Y_train) #Fit the model to your data
pred_knn_train = model_knn.predict(X_train)
pred_knn_test = model_knn.predict(X_test)

print(confusion_matrix(Y_train, Y_pred4_train))
print("***********"*5)
print(confusion_matrix(Y_test, Y_pred4_test))

print(classification_report(Y_train, Y_pred4_train))
print("***********"*5)
print(classification_report(Y_test, Y_pred4_test))

print(confusion_matrix(Y_train, pred_knn_train))
print("***********"*5)
print(confusion_matrix(Y_test, pred_knn_test))

print(classification_report(Y_train, pred_knn_train))
print("***********"*5)
print(classification_report(Y_test, pred_knn_test))

from sklearn.model_selection import cross_val_score

#roc and auc
def plot_roc(model, X_test, Y_test):
  probabilities = model.predict_proba(np.array(X_test))
  probabilities = probabilities[:, 1]
  fpr, tpr, thresholds = roc_curve(Y_test, probabilities)
  roc_auc = auc(fpr, tpr)

  plt.title('Receiver Operating Characteristic')
  plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
  plt.legend(loc = 'lower right')
  plt.plot([0, 1], [0, 1],'r--')
  plt.xlim([0, 1])
  plt.ylim([0, 1])
  plt.ylabel('True Positive Rate')
  plt.xlabel('False Positive Rate')
  plt.show()

plot_roc(rfe, X_test, Y_test)

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

# Example dataset (replace with your dataset)
# Generate some random data for binary classification
np.random.seed(42)
X = np.random.rand(1000, 20)
y = np.random.randint(2, size=1000)

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Build a simple neural network
model = Sequential()
model.add(Dense(128, activation='relu', input_shape=(X_train.shape[1],)))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

# Train the model and store the history
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Function to plot accuracy and loss
def plot_history(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(acc) + 1)

    # Plot training and validation accuracy
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    plt.plot(epochs, acc, 'bo', label='Training accuracy')
    plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    # Plot training and validation loss
    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.show()

# Plot accuracy and loss
plot_history(history)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
from keras.optimizers import SGD
model.compile(optimizer=SGD(learning_rate=0.01), loss='binary_crossentropy', metrics=['accuracy'])
model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

# Try Adam Optimizer
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
history_adam = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

# Try SGD Optimizer
model.compile(optimizer=SGD(learning_rate=0.01), loss='binary_crossentropy', metrics=['accuracy'])
history_sgd = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

# Try RMSprop Optimizer
model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
history_rmsprop = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

"""Prediction Model"""

input_data = (197.07600,206.89600,192.05500,0.00289,0.00001,0.00166,0.00168,0.00498,0.01098,0.09700,0.00563,0.00680,0.00802,0.01689,0.00339,26.77500,0.422229,0.741367,-7.348300,0.177551) #Remove extra elements to match training shape

# changing input data to a numpy array
input_data_as_numpy_array = np.asarray(input_data)

# reshape the numpy array
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

# standardize the data
std_data = scaler.transform(input_data_reshaped)

prediction = model.predict(std_data)
print(prediction)


if (prediction[0] == 0):
  print("The Person does not have Parkinsons Disease")

else:
  print("The Person has Parkinsons")

import numpy as np  # Importing numpy

# Modified input data that might lead to predicting Parkinson's disease
input_data = (230.07600,245.89600,220.05500,0.00889,0.00012,0.00766,0.00868,0.01498,0.02598,0.15000,0.01263,0.01580,0.02002,0.03089,0.00839,20.77500,0.322229,0.541367,-9.348300,0.127551)

# changing input data to a numpy array
input_data_as_numpy_array = np.asarray(input_data)

# reshape the numpy array
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

# standardize the data
std_data = scaler.transform(input_data_reshaped)

prediction = model.predict(std_data)
print(prediction)

if (prediction[0] == 0):
    print("The Person does not have Parkinson's Disease")
else:
    print("The Person has Parkinson's")