# train_model_suspicious_logins.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, RocCurveDisplay
import matplotlib.pyplot as plt

# ---------------------------------------------------
# 1. Load processed dataset
# ---------------------------------------------------
df = pd.read_csv("processed_logins.csv")
print("✅ Processed data loaded —", df.shape)

# Separate features and labels
X = df.drop("label", axis=1)
y = df["label"]

# ---------------------------------------------------
# 2. Train/test split
# ---------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape},  Test set: {X_test.shape}")

# ---------------------------------------------------
# 3. Train Random Forest model
# ---------------------------------------------------
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=8,
    class_weight="balanced",
    random_state=42
)
model.fit(X_train, y_train)

# ---------------------------------------------------
# 4. Predictions
# ---------------------------------------------------
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# ---------------------------------------------------
# 5. Evaluation
# ---------------------------------------------------
print("\n🔍 Classification Report:")
print(classification_report(y_test, y_pred, digits=3))

print("\n🧮 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

roc_auc = roc_auc_score(y_test, y_prob)
print(f"\nROC-AUC: {roc_auc:.3f}")

# ROC Curve
RocCurveDisplay.from_predictions(y_test, y_prob)
plt.title("ROC Curve — Suspicious Login Detection")
plt.show()

# ---------------------------------------------------
# 6. Feature importance
# ---------------------------------------------------
importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\n📊 Feature Importance:")
print(importances)

plt.figure(figsize=(8,4))
importances.plot(kind="bar", title="Feature Importance")
plt.tight_layout()
plt.show()
# ---------------------------------------------------
# 7. Save trained model to file
# ---------------------------------------------------
# ---------------------------------------------------
# Save trained model
# ---------------------------------------------------
import joblib
joblib.dump(model, "login_detector.pkl")
print("💾 Model saved as login_detector.pkl")

