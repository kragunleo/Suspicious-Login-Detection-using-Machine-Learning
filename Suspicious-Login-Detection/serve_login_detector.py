# serve_login_detector.py

from flask import Flask, request, jsonify
import pandas as pd
import joblib

# ---------------------------------------------------
# 1. Load trained model
# ---------------------------------------------------
model = joblib.load("login_detector.pkl")  # Save this in Step 4 after training

app = Flask(__name__)

# ---------------------------------------------------
# 2. Define expected features
# ---------------------------------------------------
FEATURES = [
    "is_fail",
    "time_diff_min",
    "device_changed",
    "country_changed",
    "recent_fail_count"
]

# ---------------------------------------------------
# 3. Health check route
# ---------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Suspicious Login Detector API is running ✅"})

# ---------------------------------------------------
# 4. Prediction route
# ---------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    """
    Expects JSON payload:
    {
      "is_fail": 0,
      "time_diff_min": 120,
      "device_changed": 1,
      "country_changed": 0,
      "recent_fail_count": 3
    }
    """
    try:
        data = request.get_json()

        # Ensure all features exist
        for f in FEATURES:
            if f not in data:
                return jsonify({"error": f"Missing field: {f}"}), 400

        df = pd.DataFrame([data])
        prediction = model.predict(df)[0]
        prob = model.predict_proba(df)[0][1]

        label = "suspicious" if prediction == 1 else "normal"
        return jsonify({
            "prediction": label,
            "probability": round(float(prob), 3)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------
# 5. Run API
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
