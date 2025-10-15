# synthetic_login_data_generator.py
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 1. Configuration
num_users = 50                  # total users simulated
num_records = 5000              # total login attempts
start_date = datetime(2025, 9, 1)
end_date = datetime(2025, 10, 1)

countries = ["Côte d'Ivoire", "Turkey", "France", "USA", "Germany", "India"]
user_agents = ["Windows/Chrome", "MacOS/Safari", "Android/Chrome", "iPhone/Safari", "Linux/Firefox"]
devices = [f"device_{i}" for i in range(1, 200)]

# 2. Helper functions
def random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

def random_ip():
    """Generate a random IPv4 address"""
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# 3. Generate normal logins
records = []
for _ in range(num_records):
    username = f"user_{random.randint(1, num_users)}"
    ts = random_date(start_date, end_date)
    country = random.choice(countries)
    device = random.choice(devices)
    ua = random.choice(user_agents)
    result = np.random.choice(["success", "fail"], p=[0.9, 0.1])  # mostly successful
    records.append([ts, username, random_ip(), country, device, ua, result, 0])  # label=0 normal

df = pd.DataFrame(records, columns=["timestamp", "username", "src_ip", "country", "device_id", "user_agent", "result", "label"])

# 4. Inject suspicious behavior
# A. Brute-force attacks
for user_id in random.sample(range(1, num_users), 5):  # pick 5 users for brute force
    for _ in range(8):
        df.loc[len(df)] = [random_date(start_date, end_date), f"user_{user_id}", random_ip(), random.choice(countries),
                           random.choice(devices), random.choice(user_agents), "fail", 1]
    df.loc[len(df)] = [random_date(start_date, end_date), f"user_{user_id}", random_ip(), random.choice(countries),
                       random.choice(devices), random.choice(user_agents), "success", 1]

# B. Impossible travel (same user, far countries within 10 min)
for user_id in random.sample(range(1, num_users), 5):
    t = random_date(start_date, end_date)
    df.loc[len(df)] = [t, f"user_{user_id}", random_ip(), "Côte d'Ivoire", random.choice(devices),
                       random.choice(user_agents), "success", 1]
    df.loc[len(df)] = [t + timedelta(minutes=5), f"user_{user_id}", random_ip(), "Germany", random.choice(devices),
                       random.choice(user_agents), "success", 1]

# C. Device change anomaly (sudden new device)
for user_id in random.sample(range(1, num_users), 5):
    t = random_date(start_date, end_date)
    df.loc[len(df)] = [t, f"user_{user_id}", random_ip(), random.choice(countries), "device_new_999",
                       random.choice(user_agents), "success", 1]

# 5. Final touches
df = df.sort_values("timestamp").reset_index(drop=True)
df["timestamp"] = df["timestamp"].astype(str)  # convert for CSV

# 6. Save to file
df.to_csv("synthetic_logins.csv", index=False)
print("✅ Synthetic dataset saved as synthetic_logins.csv")
print("Sample rows:")
print(df.head(10))
print("\nTotal suspicious records:", df['label'].sum(), "/", len(df))
