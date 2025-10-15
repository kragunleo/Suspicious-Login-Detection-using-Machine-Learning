import requests

# Example login features
data = {
    "is_fail": 1,          # did the login fail?
    "time_diff_min": 3,    # minutes since previous login
    "device_changed": 1,   # new device?
    "country_changed": 1,  # login from a different country?
    "recent_fail_count": 4 # failed attempts in last 5 logins
}

response = requests.post("http://127.0.0.1:5000/predict", json=data)
print(response.json())
