import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import requests
import json
from datetime import datetime
import pandas as pd


coor = pd.read_csv("cor.csv")


response_API = requests.get('https://api.waqi.info/feed/A193744/?token=85f56674e2fcf4355cf0da22c00f7492a91bf001')
weather_API = requests.get('http://my.meteoblue.com/packages/basic-1h_basic-day?lat=42.872530&lon=74.808407&apikey=2fbYedHr7DMCQtNR')

now = datetime.now()
d = pd.to_datetime(now)


# Create flask app
flask_app = Flask(__name__)
model = pickle.load(open("model1.pkl", "rb"))
model1 = pickle.load(open("model2.pkl", "rb"))


@flask_app.route("/")
def Home():
    return render_template("index.html")


@flask_app.route('/select', methods=['POST', 'GET'])
def select():
    value = request.form.get('operator')
    ur = coor['api'].iloc[int(value)-1]
    global response_API 
    response_API = requests.get(str(ur))
    return predict()



@flask_app.route("/predict", methods = ["POST"])
def predict():
    data = response_API.text
    parse_json = json.loads(data)
    active_case = parse_json['data']['aqi']
    current_aqi = active_case
    temp = parse_json['data']['iaqi']['t']['v']
    humid = parse_json['data']['iaqi']['h']['v']
    timey = parse_json['data']['time']['s']
    timey = pd.to_datetime(timey)

    data_weather = weather_API.text
    parse_weather = json.loads(data_weather)
    diff = abs(0 - timey.hour)+1
    # diff
    predictions = []
    t = []

    predictionsd = []
    dayss = []

    for i in range(diff, 24+diff):
        temp = parse_weather['data_1h']['temperature'][i]
        humid = parse_weather['data_1h']['relativehumidity'][i]
        tim = parse_weather['data_1h']['time'][i]
        tim = pd.to_datetime(tim)

        features = [[tim.month, tim.day, tim.hour, temp, humid, active_case]]
        prediction = model.predict(features)
        predictions.append(round(float(prediction)))
        t.append(tim.hour)
        active_case = prediction

    for j in range(0, 7):
        temp1 = parse_weather['data_day']['temperature_mean'][j]
        humid1 = parse_weather['data_day']['relativehumidity_mean'][j]
        daya = parse_weather['data_day']['time'][j]
        daya = pd.to_datetime(daya)

        features1 = [[temp1, humid1, daya.month, daya.day]]
        prediction1 = model1.predict(features1)
        predictionsd.append(round(float(prediction1)))
        dayss.append(daya)


    return render_template("index.html", 
                           
        last_updated = "Last updated at {}:00".format(timey.hour), 
        prediction_text = int(prediction), 
        aqi_now = current_aqi,
        valueh1 = predictions[0], 
        valueh2 = predictions[1],
        valueh3 = predictions[2],
        valueh4 = predictions[3],
        valueh5 = predictions[4],
        valueh6 = predictions[5],
        valueh7 = predictions[6],
        valueh8 = predictions[7],
        valueh9 = predictions[8],
        valueh10 = predictions[9],
        valueh11 = predictions[10],
        valueh12 = predictions[11],
        valueh13 = predictions[12],
        valueh14 = predictions[13],
        valueh15 = predictions[14],
        valueh16 = predictions[15],
        valueh17 = predictions[16],
        valueh18 = predictions[17],
        valueh19 = predictions[18],
        valueh20 = predictions[19],
        valueh21 = predictions[20],
        valueh22 = predictions[21],
        valueh23 = predictions[22],
        valueh24 = predictions[23],
        
        timeh1 = "{}:00".format(t[0]),
        timeh2 = "{}:00".format(t[1]),
        timeh3 = "{}:00".format(t[2]),
        timeh4 = "{}:00".format(t[3]),
        timeh5 = "{}:00".format(t[4]),
        timeh6 = "{}:00".format(t[5]),
        timeh7 = "{}:00".format(t[6]),
        timeh8 = "{}:00".format(t[7]),
        timeh9 = "{}:00".format(t[8]),
        timeh10 = "{}:00".format(t[9]),
        timeh11 = "{}:00".format(t[10]),
        timeh12 = "{}:00".format(t[11]),
        timeh13 = "{}:00".format(t[12]),
        timeh14 = "{}:00".format(t[13]),
        timeh15 = "{}:00".format(t[14]),
        timeh16 = "{}:00".format(t[15]),
        timeh17 = "{}:00".format(t[16]),
        timeh18 = "{}:00".format(t[17]),
        timeh19 = "{}:00".format(t[18]),
        timeh20 = "{}:00".format(t[19]),
        timeh21 = "{}:00".format(t[20]),
        timeh22 = "{}:00".format(t[21]),
        timeh23 = "{}:00".format(t[22]),
        timeh24 = "{}:00".format(t[23]),

        valued1 = predictionsd[0],
        valued2 = predictionsd[1],
        valued3 = predictionsd[2],
        valued4 = predictionsd[3],
        valued5 = predictionsd[4],
        valued6 = predictionsd[5],
        valued7 = predictionsd[6],
        

        day1 = dayss[0],
        day2 = dayss[1],
        day3 = dayss[2],
        day4 = dayss[3],
        day5 = dayss[4],
        day6 = dayss[5],
        day7 = dayss[6],
    
        )


if __name__ == "__main__":
    flask_app.run(debug=True)