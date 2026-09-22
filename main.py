import os
import requests
from twilio.rest import Client

api_key = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

weather_params = {
    "lat": 23.642139 ,
    "lon": 86.171681,
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(
    "https://api.openweathermap.org/data/2.5/forecast",
    params=weather_params
)

response.raise_for_status()
weather_data = response.json()

will_rain = False

for hour_data in weather_data["list"]:
    weather_id = hour_data["weather"][0]["id"]

    if weather_id < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella ☔",
        from_="+17372508034",
        to="+918540928409",
    )

    print(message.status)
