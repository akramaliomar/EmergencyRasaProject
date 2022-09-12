import requests
import tensorflow as tf
import numpy as np


def fetch_vital_signs():
    url = 'https://aceiot-project.uc.r.appspot.com/fetch_vs'
    json_data = requests.get(url).json()
    # format_add = json_data['main']
    # print(format_add)
    return json_data


def prediction(hr, spo2, resp, tempr):
    # testvalue = [[77., 93., 20., 26.]]
    testvalue = [[float(hr), float(spo2), float(resp), float(tempr)]]
    loaded_model = tf.keras.models.load_model('/app/actions/vital_signs.h5')  # loading the saved model
    predictions = loaded_model.predict(testvalue)  # making predictions
    vital_signs = int(np.argmax(predictions))  # index of maximum prediction
    probability = max(predictions.tolist()[0])  # probability of maximum prediction
    # print("Prediction: ", predictions.tolist())
    # print("Vital Sign: ", vital_signs)
    # print("Probability: ", probability)
    if vital_signs==1:
        return "Abnormal"
    elif vital_signs==0:
        return "Normal"

def fetch_aggr_signs():
    url = 'https://aceiot-project.uc.r.appspot.com/fetch_aggr_vs'
    json_data = requests.get(url).json()
    # format_add = json_data['main']
    # print(format_add)
    return json_data

# def fetch_heath_status():
#     url = 'https://aceiot-project.uc.r.appspot.com/prediction'
#     json_data = requests.get(url).json()
#     # format_add = json_data['main']
#     # print(format_add)
#     return json_data