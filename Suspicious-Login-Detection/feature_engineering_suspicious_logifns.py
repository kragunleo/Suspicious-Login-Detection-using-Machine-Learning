# feature_engineering_suspicious_logins.py

import pandas as pd
import numpy as np

# ---------------------------------------------------
# 1. Load dataset
# ---------------------------------------------------
df = pd.read_csv("synthetic_logins.csv", parse_dates=["timestamp"])
print("✅ Data loaded —", df.shape, "rows")
print(df.head(5))

# ---------------------------------------------------
# 2. Basic preprocessing
# ---------------------------------------------------
# Sort by user + time to compute behavioral patterns
df = df.sort_values(["username", "timestamp"]).reset_index(drop=True)

# Convert result to binary (1=fail, 0=success)
df["is_fail"] = (df["result"] == "fail").astype(int)

# ---------------------------------------------------
# 3. Feature Engineering (per login event)
# ---------------------------------------------------
# Group by user to calculate patterns
df["prev_country"] = df.groupby("username")["country"].shift(1)
df["prev_device"] = df.groupby("username")["device_id"].shift(1)
df["prev_time"] = df.groupby("username")["timestamp"].shift(1)

# Time difference between logins (in minutes)
df["time_diff_min"] = (df["timestamp"] - df["prev_time"]).dt.total_seconds() / 60

# Device change indicator
df["device_changed"] = (df["device_id"] != df["prev_device"]).astype(int)

# Country change indicator
df["country_changed"] = (df["country"] != df["prev_country"]).astype(int)

# Rolling failure count (last 5 attempts per user)
df["recent_fail_count"] = (
    df.groupby("username")["is_fail"]
      .rolling(window=5, min_periods=1)
      .sum()
      .reset_index(level=0, drop=True)
)

# ---------------------------------------------------
# 4. Fill NaN values (for first logins)
# ---------------------------------------------------
df["time_diff_min"].fillna(9999, inplace=True)
df.fillna(0, inplace=True)

# ---------------------------------------------------
# 5. Select ML-ready features
# ---------------------------------------------------
feature_cols = [
    "is_fail",
    "time_diff_min",
    "device_changed",
    "country_changed",
    "recent_fail_count"
]
X = df[feature_cols]
y = df["label"]

print("\n🎯 Feature sample:")
print(X.head(10))
print("\nLabel distribution:")
print(y.value_counts())

# ---------------------------------------------------
# 6. Save processed data
# ---------------------------------------------------
processed = pd.concat([X, y], axis=1)
processed.to_csv("processed_logins.csv", index=False)
print("\n✅ Saved processed dataset: processed_logins.csv")
