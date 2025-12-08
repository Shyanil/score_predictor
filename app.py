from flask import Flask,request, render_template
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData , predictPipeline
application = Flask(__name__)
app = application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata' , methods = ['GET' , 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data=CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),
            writing_score=float(request.form.get('reading_score'))

        )
        data_df = data.get_data_as_dataFrame()
        print(data_df)
        prediction_pipeline = predictPipeline()
        results = prediction_pipeline.predict(prediction_pipeline)
        return render_template('home.html' , results=results[0])


if __name__ == '__main__':
    app.run(host="0.0.0.0" , debug = True)