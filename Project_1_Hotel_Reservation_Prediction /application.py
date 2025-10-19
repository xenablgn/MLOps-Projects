import joblib
import numpy as np
from config.paths_config import MODEL_OUTPUT_DIR
from flask import Flask, render_template, request

app = Flask(__name__)

# Load model
try:
    loaded_model = joblib.load(f"{MODEL_OUTPUT_DIR}/xgboost_model.joblib")
except Exception as e:
    loaded_model = None
    print(f"Error loading model: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    prediction_text = None

    if request.method == "POST":
        try:

            lead_time = int(request.form["lead_time"])
            no_of_special_requests = int(request.form["no_of_special_requests"])
            avg_price_per_room = float(request.form["avg_price_per_room"])
            arrival_month = int(request.form["arrival_month"])
            arrival_date = int(request.form["arrival_date"])
            no_of_week_nights = int(request.form["no_of_week_nights"])
            market_segment_type = int(request.form["market_segment_type"])
            no_of_weekend_nights = int(request.form["no_of_weekend_nights"])
            arrival_year = int(request.form["arrival_year"])
            no_of_adults = int(request.form["no_of_adults"])

            features = np.array([[
                lead_time,
                no_of_special_requests,
                avg_price_per_room,
                arrival_month,
                arrival_date,
                no_of_week_nights,
                market_segment_type,
                no_of_weekend_nights,
                arrival_year,
                no_of_adults
            ]])

            # Make prediction
            if loaded_model is not None:
                prediction = loaded_model.predict(features)[0]  # 0 or 1
                prediction_text = (
                    "Customer is going to CANCEL the booking ❌"
                    if prediction == 1
                    else "Customer is NOT going to cancel the booking ✅"
                )
            else:
                prediction_text = "Model not loaded. Cannot make prediction."
        except Exception as e:
            prediction_text = f"Error in prediction: {e}"

    return render_template("index.html", prediction=prediction, prediction_text=prediction_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
