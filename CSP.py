import pandas as pd  
import numpy as np 
import seaborn as sns
from matplotlib import pyplot
from utils import *
#Importing DataSet
dataset = pd.read_csv("CAS_Data_1.csv", nrows = 200000)
#dataset.head()  
#print(dataset.dtypes)


#preparing Data for training
                 
X = dataset.iloc[:, 0:16].values
y = dataset.iloc[:, 16].values

#Dividing Data into Training and Testing
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
print(pd.Series(y).value_counts(),"\n\n\n")


# Feature Scaling
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()  
X_train = sc.fit_transform(X_train)  
X_test = sc.transform(X_test)

#Training the Algorithm

from sklearn.ensemble import RandomForestClassifier

classifier = RandomForestClassifier(n_estimators=100, random_state=0)
classifier.fit(X_train, y_train)  
y_pred = classifier.predict(X_test)

#Getting Accurecy, Precision, Recall and F1_score

RF_base_original_metrics = structure_and_print_results('RF Baseline', 'Original', y_test, y_pred, digits=5)



