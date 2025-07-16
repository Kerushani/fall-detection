import pandas as pd
import numpy as np
import matplotlib as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib


#dataset link: https://www.kaggle.com/datasets/antonygarciag/walker-fall-detection?resource=download
data = pd.read_csv(r'/Users/kerushanisivaneswaran/Documents/GitHub/fall-detection/fall_data.csv')


# Assuming df is your DataFrame
acc_x_cols = [f'acc_x_{i}' for i in range(160)]
acc_y_cols = [f'acc_y_{i}' for i in range(160)]
acc_z_cols = [f'acc_z_{i}' for i in range(160)]
gy_x_cols = [f'gy_x_{i}' for i in range(160)]
gy_y_cols = [f'gy_y_{i}' for i in range(160)]
gy_z_cols = [f'gy_z_{i}' for i in range(160)]

# Compute row-wise means for each direction
data['acc_x_avg'] = data[acc_x_cols].mean(axis=1)
data['acc_y_avg'] = data[acc_y_cols].mean(axis=1)
data['acc_z_avg'] = data[acc_z_cols].mean(axis=1)
data['gy_x_avg'] = data[gy_x_cols].mean(axis=1)
data['gy_y_avg'] = data[gy_y_cols].mean(axis=1)
data['gy_z_avg'] = data[gy_z_cols].mean(axis=1)

keep_cols = ['label', 'acc_x_avg', 'acc_y_avg', 'acc_z_avg', 'gy_x_avg', 'gy_y_avg', 'gy_z_avg']

data = data[keep_cols]
data.rename(columns=dict(zip(['label', 'acc_x_avg', 'acc_y_avg', 'acc_z_avg', 'gy_x_avg', 'gy_y_avg', 'gy_z_avg'], ['label', 'xa', 'ya', 'za', 'xg', 'yg', 'zg'])), inplace=True)

data['is_fall'] = (data['label'] == 'fall').astype(int)

#Features and target
X = data[["xa", "ya", "za" ,"xg", "yg", "zg"]]
y = data['is_fall']

#Create and train the classifier
clf = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    class_weight='balanced',
    random_state=42
)

clf.fit(X, y)

#Save the trained model to a file
joblib.dump(clf, 'fall_detection_model.pkl')