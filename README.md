# Suspicious-Login-Detection-using-Machine-Learning  
Detect suspicious login attempts using a Random Forest classifier trained on synthetic authentication logs. This project demonstrates an end-to-end machine learning pipeline for cybersecurity: data generation, feature engineering, model training, evaluation, and a real-time prediction API.

🔹 Features

Generate synthetic login datasets with normal and malicious patterns:

Brute-force attacks

Impossible travel (same user, far countries in a short time)

Device change anomalies

Extract behavioral features for detection:

Failed login counts

Time difference between logins

Device and country change flags

Train and evaluate a Random Forest classifier:

Precision, recall, F1-score

Confusion matrix and ROC-AUC

Deploy a Flask API for real-time predictions

Beginner-friendly, fully reproducible

📁 Project Structure
Suspicious-Login-Detection/
│
├─ synthetic_login_data_generator.py   # Generate synthetic login dataset
├─ processed_logins.csv                # Feature-engineered dataset
├─ train_model_suspicious_logins.py   # Train and evaluate Random Forest
├─ login_detector.pkl                  # Saved trained model
├─ serve_login_detector.py             # Flask API for real-time predictions
└─ README.md                           # Project documentation

🛠️ Installation

Clone the repository:

git clone https://github.com/yourusername/Suspicious-Login-Detection.git
cd Suspicious-Login-Detection


Create a virtual environment (optional but recommended):

python -m venv venv
# Activate on Windows
venv\Scripts\activate
# Activate on Linux/Mac
source venv/bin/activate


Install dependencies:

pip install pandas numpy scikit-learn matplotlib flask joblib

⚡ Usage
1. Generate synthetic login dataset
python synthetic_login_data_generator.py


Generates synthetic_logins.csv with normal and malicious login attempts.

2. Feature engineering & preprocessing

Use your preprocessing notebook or script to create processed_logins.csv

Includes features such as is_fail, time_diff_min, device_changed, country_changed, recent_fail_count.

3. Train the model
python train_model_suspicious_logins.py


Trains a Random Forest classifier

Saves trained model as login_detector.pkl

Prints evaluation metrics (precision, recall, F1, ROC-AUC, confusion matrix)

4. Run Flask API for real-time detection
python serve_login_detector.py


API runs at: http://127.0.0.1:5000

Health check: GET /

Prediction endpoint: POST /predict with JSON payload

Example request:
{
  "is_fail": 1,
  "time_diff_min": 3,
  "device_changed": 1,
  "country_changed": 1,
  "recent_fail_count": 4
}

Example response:
{
  "prediction": "suspicious",
  "probability": 0.85
}

📊 Evaluation Metrics

Accuracy, precision, recall, F1-score

ROC-AUC ~0.80 (can be improved with more data or hyperparameter tuning)

Feature importance:

recent_fail_count

time_diff_min

device_changed

country_changed

🔧 Notes

Designed for learning and portfolio demonstration — not production-ready

Synthetic data can be extended with more patterns or real anonymized logs

Model can be replaced with XGBoost, LightGBM, or neural networks for improvement

📚 References

Scikit-learn RandomForestClassifier

Flask Documentation

Synthetic Data Generation in Python
