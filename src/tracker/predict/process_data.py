import os
import numpy as np
import pandas as pd

from tracker.predict.model import Model
from tracker.db.db import Models, Money
from tracker.db.utils import session_scope
from tracker.consts import Consts


def load_data_from_file():
    return pd.read_csv(Consts.CSV_FILE, sep=';')

def prepare_data(data:pd.DataFrame, from_file = False)->pd.DataFrame:
    if len(data) == 0:
        raise Exception('Empty DataFrame')
    
    if from_file:
        data.drop([Consts.FLAT_COLUMN, Consts.SHOP_COLUMN, Consts.FUN_COLUMN, Consts.GOOUT_COLUMN], axis = 1)  
        
    for dt in data:
        temp_mean = data[dt].mean()
        data[dt] = data[dt].replace(0, temp_mean)
    
    return data

def load_data_from_db():...

def remove_model(model_name):
    if not os.path.exists(f'{Consts.MODELS_PATH}/{model_name}'):
        os.remove(f'{Consts.MODELS_PATH}/{model_name}')



