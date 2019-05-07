from weather import *
import requests
from weather.models import City


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        new_city = request.form['city']

        new_city_obj = City(name=new_city)

        db.session.add(new_city_obj)
        db.session.commit()
        return redirect(url_for('index'))
    cities = City.query.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city.name)).json()
        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(weather)
    return render_template('weather.html', weather_data=weather_data)
