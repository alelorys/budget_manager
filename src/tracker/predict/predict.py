import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def predict_budget():
    data = pd.read_csv(r'C:\Users\alorys\Documents\programowanie\python\AI\tracker_wydatkow_2\src\tracker\predict\budzet-2.csv',
                   sep=';')
    Y = data['Suma']
    Y = Y[:-1]
    data.drop(columns=['Suma','Mieszkanie','Zakupy','Rekreacja'], inplace=True)
    X = data[:-1]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.1, random_state = 1)

    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    return regressor, data.iloc[-1]
