import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from src.logger import logger
from src.exception import custom_Exception

@dataclass
class DataTransformationConfig:
    preprocessor_obj_path = os.path.join('artifacts' , 'preprocessor.pkl')