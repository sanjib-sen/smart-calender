# importing modules
import requests, json

# API base URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

# City Name
CITY = "New Delhi"

# Your API key
API_KEY = "c97d8fcb636e4777934f533570419b9e"

# updating the URL
URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY

def get_weather_data():
    # Sending HTTP request
    response = requests.get(URL)

    # checking the status code of the request
    if response.status_code == 200:

        # retrieving data in the json format
        data = response.json()

        # take the main dict block
        main = data['main']

        # getting temperature
        temperature = main['temp']
        # getting feel like
        temp_feel_like = main['feels_like']
        # getting the humidity
        humidity = main['humidity']
        # getting the pressure
        pressure = main['pressure']

        # weather report
        weather_report = data['weather']
        # wind report
        wind_report = data['wind']

        # print(f"{CITY:-^35}")
        # print(f"City ID: {data['id']}")
        # print(f"Temperature: {temperature}")
        # print(f"Feel Like: {temp_feel_like}")
        # print(f"Humidity: {humidity}")
        # print(f"Pressure: {pressure}")
        # print(f"Weather Report: {weather_report[0]['description']}")
        # print(f"Wind Speed: {wind_report['speed']}")
        # print(f"Time Zone: {data['timezone']}")

        return temperature
    else:
        # showing the error message
        print("Error in the HTTP request")