from flask import Flask, jsonify, request
from db import db_add_vs, db_get_vs, db_aggregated_vs
import numpy as np
import tensorflow as tf

app = Flask(__name__)


@app.route('/')
def hello():
    return "hello world"


@app.route('/fetch_vs', methods=['GET'])
def get_vital_signs():
    return db_get_vs()


@app.route('/fetch_aggr_vs', methods=['GET'])
def get_aggregated_vs():
    return db_aggregated_vs()


@app.route('/prediction', methods=['GET'])
def get_prediction_vs():
    testvalue = [[77., 93., 20., 26.]]

    loaded_model = tf.keras.models.load_model('vital_signs.h5')  # loading the saved model
    predictions = loaded_model.predict(testvalue)  # making predictions
    vital_signs = int(np.argmax(predictions))  # index of maximum prediction
    probability = max(predictions.tolist()[0])  # probability of maximum prediction
    # print("Prediction: ", predictions.tolist())
    # print("Vital Sign: ", vital_signs)
    # print("Probability: ", probability)
    return jsonify(vital_signs)


@app.route('/add_vs', methods=['POST'])
def add_vital_signs():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    db_add_vs(request.get_json())
    return "Vital Signs added"


if __name__ == "__main__":
    app.run()
