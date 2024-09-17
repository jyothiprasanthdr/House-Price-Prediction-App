import pickle
from flask import Flask, request, app, jsonify, url_for, render_template
import numpy as np
import pandas as pd
from flask_cors import CORS


app = Flask(__name__)

CORS(app)


regmodel = pickle.load(open("model.pickle", "rb"))
scalar = pickle.load(open("scaler.pickle", "rb"))
encoder = pickle.load(open("encoder.pickle", "rb"))


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


@app.route("/predict", methods=["POST"])
def predict():
    # Get the form values from the POST request
    data = list(request.form.values())
    print(data)

    # Separate numerical and categorical data
    num_data = data[0:4]  # First 5 are numerical data
    cat_data = [data[4], data[5]]  # Last 2 are categorical (e.g., State, HomeType)

    # Convert numerical data to float and reshape it to a 2D array
    try:
        num_data = np.array(num_data, dtype=float).reshape(1, -1)  # Convert and reshape
    except ValueError:
        return "Error: Please enter valid numerical values."

    # Encode numerical and categorical data
    encoded_num = scalar.transform(num_data)  # Scale numerical features
    encoded_cat = encoder.transform([cat_data])  # Encode categorical features

    # Concatenate encoded numerical and categorical features
    input_data = np.concatenate([encoded_num, encoded_cat], axis=1)

    # Make prediction
    output = regmodel.predict(input_data)[0]

    # Render the result in the template
    return render_template(
        "home.html",
        prediction_text="The House Price Prediction is ${:.2f}".format(output),
    )


if __name__ == "__main__":
    app.run(debug=True)
