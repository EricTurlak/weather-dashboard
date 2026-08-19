from datetime import datetime
from zoneinfo import ZoneInfo
import requests

city = input("Enter City: ")

coordinatesResponse = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=en&format=json")
coordinatesResponse.raise_for_status()
coordinatesData = coordinatesResponse.json()

while "results" not in coordinatesData or not coordinatesData["results"]:
    print(f"No results found for {city}")
    city = input("Enter City: ")
    coordinatesResponse = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=en&format=json")
    coordinatesResponse.raise_for_status()
    coordinatesData = coordinatesResponse.json()

if len(coordinatesData["results"]) > 1:
    for count, result in enumerate(coordinatesData["results"], start=1):
        print(f"{count}. {result['name']}, {result['admin1']}")

    pickedNum = input(f"More than one result found for {city}. Please input the number of the correct city: ")

    while not pickedNum.isdigit() or not 1 <= int(pickedNum) <= len(coordinatesData["results"]):
        pickedNum = input(f"Please enter a valid number: ")
    latitude = coordinatesData["results"][int(pickedNum) - 1]["latitude"]
    longitude = coordinatesData["results"][int(pickedNum) - 1]["longitude"]
    timezone = coordinatesData["results"][int(pickedNum) - 1]["timezone"]
else:
    latitude = (coordinatesData["results"][0]["latitude"])
    longitude = (coordinatesData["results"][0]["longitude"])
    timezone = (coordinatesData["results"][0]["timezone"])

url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&timezone={timezone}&wind_speed_unit=mph&temperature_unit=fahrenheit&precipitation_unit=inch"
response = requests.get(url)
response.raise_for_status()
data = response.json()
currentHour = datetime.now(ZoneInfo(timezone)).strftime("%Y-%m-%dT%H:00")
temp = data['hourly']['temperature_2m']
time = data['hourly']['time']

for index, hour in enumerate(time):
    if hour == currentHour:
        print(f"Temperature is currently: {temp[index]}°F")
