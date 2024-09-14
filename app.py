import pickle
from flask import Flask, request, app, jsonify, url_for, render_template
import numpy as np
import pandas as pd


from flask_cors import CORS

app = Flask(__name__)
CORS(app)


regmodel = pickle.load(open("model.pkl", "rb"))
scalar = pickle.load(open("scaler.pkl", "rb"))
encoder = pickle.load(open("encoder.pkl", "rb"))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict_api", methods=["POST"])
def predict_api():
    json_data = request.get_json()
    data = json_data["data"]

    cat_values = [[data["State"], data["HomeType"]]]
    encoded_cat = encoder.transform(cat_values)

    num_values = [
        [
            data["AnnualInsurance"],
            data["YearBuilt"],
            data["LivingArea"],
            data["Bathrooms"],
            data["Bedrooms"],
        ]
    ]
    encoded_num = scalar.transform(num_values)
    input_data = np.concatenate([encoded_num, encoded_cat], axis=1)
    output = regmodel.predict(input_data)

    print(output[0])
    return jsonify(output[0])


if __name__ == "__main__":
    app.run(debug=True)
