import os
import pathlib
import datetime
import pickle
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from tracker.consts import Consts

class Model:

    def build_model():
        return LinearRegression()
    
    def train_model(model, data):
        X = data.drop(['Suma'], axis=1)
        y = data['Suma']
        x, x_test, y, y_test = train_test_split(X, y, test_size=0.1)
        return model.fit(x, y)
    
    def save_model(model)->dict:
        date = datetime.datetime.now()
        model_name = f'model-{date}.sav'
        model_path = 'C:/Users/aleks/Documents/programowanie/Python/AI/budget_manager/src/tracker/models/' + model_name.replace(":",".")
        with open(model_path, 'wb') as file:
            pickle.dump(model,file)
        return {"model_name":model_name, "date":date, "model_path":model_path}

    def load_model( model_name):
        return pickle.load(open(os.path.join(Consts.MODELS_PATH,model_name), 'rb'))

    def predict(model, data):
        return model.predict(data)