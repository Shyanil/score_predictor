from src.exception import custom_Exception
import os
import dill
import sys
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import pickle
def save_obj(file_path , obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path , exist_ok=True)
        with open(file_path , "wb") as file_obj:
            dill.dump(obj , file_obj)
    except Exception as e:
        raise custom_Exception(e, sys)


def evaluateModel(X_train , y_train , X_test, y_test , models, params):
    try:
        report = {}
        for model_name , model in models.items():
            model_params = params.get(model_name , {})

            if model_name:
                gs = GridSearchCV(model , model_params , cv=3)
                gs.fit(X_train , y_train)

                model.set_params(**gs.best_params_)

            model.fit(X_test , y_test)
            y_pred = model.predict(X_test)
            
            score = r2_score(y_true=y_test , y_pred=y_pred)
            report[model_name] = score
        
        return report    
    except Exception as e:
        raise custom_Exception(e , sys)


def load_object(file_path):
    try:
        with open(file_path , "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise custom_Exception(e , sys)
