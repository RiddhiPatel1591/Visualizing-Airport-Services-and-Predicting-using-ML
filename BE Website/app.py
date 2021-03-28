# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 15:25:27 2021

@author: MS.PRIYANKA
"""


import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
flightdelay = pickle.load(open('FlightDelay.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('Passenger.html')

@app.route('/predict',methods=['POST'])
def predict():
    
    int_features = request.form.values(departure_date_time,origin,destination)
    final_features = [np.array(int_features)]
    
    from datetime import datetime
    
    try:
        departure_date_time_parsed = datetime.strptime(departure_date_time, '%d/%m/%Y %H:%M:%S')
    except ValueError as e:
        return 'Error parsing date/time - {}'.format(e)
    
    month = departure_date_time_parsed.month
    day = departure_date_time_parsed.day
    day_of_week = departure_date_time_parsed.isoweekday()
    hour = departure_date_time_parsed.hour
    
    
    origin = origin.upper()
    destination = destination.upper()
    
    input = [{'MONTH':month,
             'DAY' : day,
             'DAY_OF_WEEK' : day_of_week,
             'CRS_DEP_TIME' : hour,
             'ORIGIN_ATL': 1 if origin == 'ATL' else 0,
             'ORIGIN_DTW': 1 if origin == 'DTW' else 0,
             'ORIGIN_JFK': 1 if origin == 'JFK' else 0,
             'ORIGIN_MSP': 1 if origin == 'MSP' else 0,
             'ORIGIN_SEA': 1 if origin == 'SEA' else 0,
             'DEST_ATL': 1 if destination == 'ATL' else 0,
             'DEST_DTW': 1 if destination == 'DTW' else 0,
             'DEST_JFK': 1 if destination == 'JFK' else 0,
             'DEST_MSP': 1 if destination == 'MSP' else 0,
             'DEST_SEA': 1 if destination == 'SEA' else 0}]
    output = flightdelay.predict_proba(pd.DataFrame(input))[0][0]
    return render_template('Passenger.html', prediction_text='Flight Prediction $ {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)
    
    



        