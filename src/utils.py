from src.exception import custom_Exception
import os
import dill
import sys
def save_obj(file_path , obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(file_path , exist_ok=True)
        with open("file_path" , "wb") as file_obj:
            dill.dump(obj , file_obj)
    except Exception as e:
        raise custom_Exception(e, sys)
