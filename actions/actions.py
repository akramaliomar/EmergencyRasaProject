import requests, json


def fetch_vital_signs(device_no):
    r = requests.post('http://154.53.40.198:8080/api/fetch_vs', json={'deviceNo': device_no})
    return r.json()


def authenticate_device(device_no, device_code):
    r = requests.post('http://154.53.40.198:8080/api/authenticate_device_user', json={'deviceNo': device_no, "device_key": device_code})
    return r.json()


def optimize_slots(myslot):
    if type(myslot) == list:
        if "DVS" in myslot:
            myslot.remove("DVS")
        return ''.join(myslot)
    else:
        return myslot



# def prediction(hr, spo2, resp, tempr):
#     # testvalue = [[77., 93., 20., 26.]]
#     testvalue = [[float(hr), float(spo2), float(resp), float(tempr)]]
#     loaded_model = tf.keras.models.load_model('/app/actions/vital_signs.h5')  # loading the saved model
#     predictions = loaded_model.predict(testvalue)  # making predictions
#     vital_signs = int(np.argmax(predictions))  # index of maximum prediction
#     probability = max(predictions.tolist()[0])  # probability of maximum prediction
#     # print("Prediction: ", predictions.tolist())
#     # print("Vital Sign: ", vital_signs)
#     # print("Probability: ", probability)
#     if vital_signs==1:
#         return "Abnormal"
#     elif vital_signs==0:
#         return "Normal"

# def fetch_aggr_signs():
#     url = 'http://localhost:8080/api/fetch_aggr_vs'
#     json_data = requests.get(url).json()
#     # format_add = json_data['main']
#     # print(format_add)
#     return json_data


# def fetch_heath_status():
#     url = 'https://aceiot-project.uc.r.appspot.com/prediction'
#     json_data = requests.get(url).json()
#     # format_add = json_data['main']
#     # print(format_add)
#     return json_data


def check_anomalies(device_no):
    r = requests.post('http://154.53.40.198:8080/api/predict_anomaly', json={'deviceNo': device_no})
    # return json.dumps(r.json())
    return r.json()
    # print(json.dumps(json_data.json()))
    # if json_data.ok:
    #     return (json_data.json())
    # # json_data = requests.get(url).json()
    #
    # # format_add = json_data['main']


def check_anomaly_recommendations(device_no, age, context, health):
    r = requests.post('http://154.53.40.198:8080/api/get_recommendtions_vs', json={'deviceNo': device_no, 'age': age, 'context': context, 'health': health})
    # json_data = requests.get(url).json()
    # format_add = json_data['main']
    # print(format_add)
    return r.json()

