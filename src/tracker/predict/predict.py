import os
import calendar
import pandas as pd
import numpy as np

from typing import Union, List

from datetime import datetime, date
from sqlalchemy import and_, func

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from tracker.db.utils import session_scope
from tracker.db.db import Money
from tracker.consts import Consts


def get_data_from_file(path):
    if os.path.exists(path):
        df = pd.read_csv(path, sep=';')

        data = df.to_dict('records')
        
        return data, list(df.columns)
            

def train_model():
    
    data:pd.DataFrame = pd.DataFrame.from_dict(get_categories_from_db()[0], orient='columns')
    data = data.fillna(0)
    Y = data['Suma']
    Y = Y[:-1]
    data.drop(columns=['Suma'], inplace=True)
    X = data[:-1]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.1, random_state = 1)

    regressor = LinearRegression()
    regressor.fit(X_train.values, y_train.values)

    return regressor

def get_last_month():
    year = datetime.now().year
    month = datetime.now().month
    month -= 1

    num_days = calendar.monthrange(year, month)[1]
    days = [date(year,month, day) for day in range(1,num_days+1)]

    return days, month

def get_categories_from_db():

    days,month = get_last_month()
    data, categories_list = get_data_from_file(Consts.CSV_FILE)
    categories_dict = {}
    with session_scope() as session:
        payments = session.query(Money.category, Money.amount).filter(Money.date.between(
            days[0],days[-1]
        )).all()
        
        total = [pay[1] for pay in payments]
        
        for cat in categories_list:
            categories_dict[cat] = 0
            if cat == 'Miesiąc':
                categories_dict[cat] = month

        for pay in payments:
            if pay[0] not in categories_dict:categories_dict[pay[0]]=pay[1]
            elif pay[0] in categories_dict:categories_dict[pay[0]]+=pay[1]

        categories_dict['Suma'] = sum(total)
    data.append(categories_dict)
    
    
    df = pd.DataFrame.from_dict([categories_dict], orient='columns')
    
    return data, df

def predict():
    model = train_model()
    df:pd.DataFrame = get_categories_from_db()[1]
    df.drop(columns=['Suma'], inplace=True)
    result = model.predict(df.values)
    
    return round(result[0], 2)

predict()

