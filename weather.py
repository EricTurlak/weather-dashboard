from datetime import datetime
import requests

city = input("Enter City: ")

coordinatesResponse = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=en&format=json")
coordinatesResponse.raise_for_status()
coordinatesData = coordinatesResponse.json()
while "results" not in coordinatesData:
    print(f"No results found for {city}")
    city = input("Enter City: ")
    coordinatesResponse = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=en&format=json")
    coordinatesResponse.raise_for_status()
    coordinatesData = coordinatesResponse.json()
latitude = (coordinatesData["results"][0]["latitude"])
longitude = (coordinatesData["results"][0]["longitude"])

url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&timezone=America%2FNew_York&wind_speed_unit=mph&temperature_unit=fahrenheit&precipitation_unit=inch"
response = requests.get(url)
response.raise_for_status()
data = response.json()

currentHour = datetime.now().strftime("%Y-%m-%dT%H:00")

temp = data['hourly']['temperature_2m']
time = data['hourly']['time']

for index, hour in enumerate(time):
    if hour == currentHour:
        print(f"Temperature is currently: {temp[index]}°F")
