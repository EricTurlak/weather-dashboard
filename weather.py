from datetime import datetime
import requests

latitude = "38.897957"
longitude = "-77.036560"

url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&timezone=America%2FNew_York&wind_speed_unit=mph&temperature_unit=fahrenheit&precipitation_unit=inch"
response = requests.get(url)
response.raise_for_status()
data = response.json()

currentHour = datetime.now().strftime("%Y-%m-%dT%H:00")

temp = data['hourly']['temperature_2m']
time = data['hourly']['time']

for index, hour in enumerate(time):
    if hour == currentHour:
        print(f"Temperature is currently: {temp[index]} degrees F")