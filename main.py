import requests
import os

from twilio.rest import Client
account_sid = 'ACed14ae15072c49c76eeab625db8144fb'
auth_token = os.environ.get("AUTH_TOKEN")

MAR_VISTA_LAT = 34.019455
MAR_VISTA_LON = -118.491188

endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API_KEY")
parameters = {
    "lat": MAR_VISTA_LAT,
    "lon": MAR_VISTA_LON,
    "appid": api_key,
    "cnt": 4 # This gives every 3 hours totalling to 12 hour weather data,
}

response = requests.get(endpoint, params=parameters)
response.raise_for_status()
# print(f"Status code: {response.status_code}")

weather_data = response.json()
# print(weather_data)

# If weather id < 700, this means there is snow, rain, drizzle or thunderstorm.
will_rain = False
for i in weather_data["list"]:
    weather_id = i["weather"][0]["id"]
    if weather_id < 700:
        will_rain = True
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        to='whatsapp:+19178853233',
        body="Bring an umbrella, it's going to rain!",
    )
    print(message.sid)
