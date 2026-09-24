import os
import smtplib
import requests
from email.message import EmailMessage
from twilio.rest import Client

SENDERS_EMAIL = os.environ.get("SENDERS_EMAIL")
RECEIVERS_EMAIL = os.environ.get("RECEIVERS_EMAIL")
PASSWORD = os.environ.get("PASSWORD")

api_key = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

client = Client(account_sid, auth_token)

OWM_endpoint = "https://api.openweathermap.org/data/2.5/forecast"

parameter = {
    "lat": 23.642139,
    "lon": 86.171681,
    "appid": api_key,
    "cnt": 4
}

response = requests.get(OWM_endpoint, params=parameter)
response.raise_for_status()
weather_data = response.json()

rain_data = weather_data["list"][0]["weather"][0]["id"]
print(rain_data)

will_rain = False

for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]

    if condition_code < 700:
        will_rain = True

if will_rain:
    try:
        message = client.messages.create(
            to="+918540928409",
            from_="+17372508034",
            body="It's going to rain today. Remember to bring an umbrella ☔",
        )

        print(message.status)

    except:
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()

        connection.login(
            user=SENDERS_EMAIL,
            password=PASSWORD
        )

        email = EmailMessage()
        email["Subject"] = "Rain Alert..☔ Carry an Umbrella"
        email["From"] = SENDERS_EMAIL
        email["To"] = RECEIVERS_EMAIL

        email.set_content(
            "It's going to rain today. Remember to carry an umbrella. "
            "Take care and don't get sick! ❤️"
        )

        connection.send_message(email)
        connection.close()

        print("Email sent!")
