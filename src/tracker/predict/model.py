import os
import datetime
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from tracker.consts import Consts

class Model:

    def __init__(self):
        super.__init__(self)

    def build_model(self):
        return LinearRegression()
    
    def train_model(self, model, x, y):
        return model.fit(x, y)
    
    def save_model(self, model):
        date = datetime.datetime.now()
        model_name = f'model-{date}.sav'
        pickle.dump(model,open(f'{Consts.MODELS_PATH}\{model_name}', 'wb'))

    def load_model(self, model_name):
        return pickle.load(open(f'{Consts.MODELS_PATH}\{model_name}', 'rb'))

    def predict(self, model, data):
        return model.predict(data)