import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import precision_score, recall_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

nrows=50000

def balancing(data, label1: str, label2: str):
    label1_data = data[data[label1] == 1]
    label2_data = data[data[label2] == 1]
    min_length = min(len(label1_data), len(label2_data))
    balanced_data = pd.concat([label1_data.sample(min_length, random_state=42),
                               label2_data.sample(min_length, random_state=42)])
    balanced_data = balanced_data.sample(frac=1, random_state=42).reset_index(drop=True)
    return balanced_data


def creating_labels(data, label1: str, label2: str):
    labels = np.where(
        data[label1] == 1, 0,
        0) + np.where(
        data[label2] == 1, 1, 0)
    return labels


def creating_smoothed_flux(data):
    flux = data[[f'flux_{i}' for i in range(2400)]]
    flux_smoothed = flux.T.rolling(window=5, min_periods=1, center=True).mean().T
    return flux_smoothed

# splitting the data to training and test sets

features_and_labels_train = pd.read_csv('all_data_flattened.csv', delimiter=' ', header=None, nrows=nrows)

columns = ['elliptical', 'spiral', 'uncertain'] + [f'flux_{i}' for i in range(2400)]

# renaming columns
features_and_labels_train.columns = columns


# selecting data with labels elliptical and spiral only, with equal number of samples in each class
train_data = balancing(features_and_labels_train, 'spiral', 'uncertain')

# separating labels and converting it to the numpy array
labels = creating_labels(train_data, 'spiral', 'uncertain')

# separate smoothed flux
flux = creating_smoothed_flux(train_data)

# Initialize the Random Forest Classifier
clf = RandomForestClassifier(n_estimators=1000, max_depth=20, class_weight='balanced')

# train and cross-validate
y_train_pred = cross_val_predict(clf, flux, labels, cv=3)

print(classification_report(labels, y_train_pred))

# extracting feature importance measure
clf.fit(flux,labels)
importances=pd.Series(clf.feature_importances_)
importances.plot(xlabel='Feature',ylabel='Importance')
plt.show()