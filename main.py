import os
import smtplib
import requests
from email.message import EmailMessage


SENDERS_EMAIL = os.environ.get("SENDERS_EMAIL")
RECEIVERS_EMAIL = os.environ.get("RECEIVERS_EMAIL")
PASSWORD = os.environ.get("EMAIL_PASSWORD")

api_key = os.environ.get("OWM_API_KEY")


OWM_endpoint = "https://api.openweathermap.org/data/2.5/forecast"

parameter = {
    "lat": 23.642139,
    "lon": 86.171681,
    "appid": api_key,
    "cnt": 8
}


response = requests.get(OWM_endpoint, params=parameter)
response.raise_for_status()
weather_data = response.json()


will_rain = False

for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    print(condition_code)

    if condition_code < 700:
        will_rain = True


if will_rain:

    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()

    connection.login(
        user=SENDERS_EMAIL,
        password=PASSWORD
    )

    email = EmailMessage()
    email["Subject"] = "🌧️ A Little Rainy-Day Reminder — Chas, Bokaro"
    email["From"] = SENDERS_EMAIL
    email["To"] = RECEIVERS_EMAIL

    email.set_content(
    "🌧️ RAINY-DAY REMINDER\n\n"
    "Hey Sis! ❤️ Just a little heads-up for you.\n\n"
    "📍 Location: Chas, Bokaro, Jharkhand\n\n"
    "It looks like rain is expected in the next 3 hours, "
    "so if you're heading out, don't forget to take an umbrella with you! ☂️\n\n"
    "Stay dry, stay cozy, and have a lovely day. 💙\n\n"
    "— Saleha 🌦️"
   )

    connection.send_message(email)
    connection.close()

    print("Email sent!")

else:
    print("No rain expected.")
