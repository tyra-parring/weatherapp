from flask import Flask, jsonify, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

api_key = "7242ec6dde87bc87a9901401066f78af"

@app.route('/')
def home():                                                                                                                                                                                                                                                                                                               
    return "Welcome to the Flask API tutorial!"

@app.route('/api/data')
def get_data():
    city = request.args.get('city','Cape Town')
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()

        city_info = {
            "name": data["city"]["name"],
            "country": data["city"]["country"]
        }

        daily_forecast = []
        for forecast in data["list"]:
            if "12:00:00" in forecast["dt_txt"]:  # Get midday readings only
                daily_forecast.append({
                    "date": datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%A, %d %B"),
                    "temperature": forecast["main"]["temp"],
                    "humidity": forecast["main"]["humidity"],
                    "wind_speed": forecast["wind"]["speed"],
                    "description": forecast["weather"][0]["description"].title(),
                    "icon": forecast["weather"][0]["icon"]
                })

        return render_template('data.html', city=city_info, forecast=daily_forecast)

    except requests.exceptions.HTTPError as http_err:
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
    except Exception as err:
        return jsonify({'error': f'Other error occurred: {err}'}), 500
    

if __name__ == '__main__':
    app.run()
