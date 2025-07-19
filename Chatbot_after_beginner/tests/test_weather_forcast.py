import unittest
from unittest.mock import patch
from src.weather_forcast import get_weather_forecast

class TestWeatherForecast(unittest.TestCase):
    def test_get_weather_forecast(self):
        # Test case 1: Valid location
        location = "city: Berlin, date: 01-01-2022, location: Germany"
        expected_output = "Weather in Berlin - Temperature: 75°F, Description: Sunny, Wind Speed: 5 mph, Humidity: 50%"
        
        with patch('src.weather_forcast.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                'name': 'Berlin',
                'main': {'temp': 75, 'humidity': 50},
                'weather': [{'description': 'Sunny'}],
                'wind': {'speed': 5}
            }
            
            forecast = get_weather_forecast(location)
            
            self.assertEqual(forecast, expected_output)
            mock_get.assert_called_once_with('https://open-weather13.p.rapidapi.com/city/Berlin', headers={'X-RapidAPI-Key': 'd9f93d0cbbmsh6495b8b1beac76ep1b16e9jsn4956b21abca2', 'X-RapidAPI-Host': 'open-weather13.p.rapidapi.com'})

        # Test case 2: Invalid location
        location = "city: InvalidCity, date: 01-01-2022, location: Germany"
        expected_output = "Error: 404"
        
        with patch('src.weather_forcast.requests.get') as mock_get:
            mock_get.return_value.status_code = 404
            
            forecast = get_weather_forecast(location)
            
            self.assertEqual(forecast, expected_output)
            mock_get.assert_called_once_with('https://open-weather13.p.rapidapi.com/city/InvalidCity', headers={'X-RapidAPI-Key': 'd9f93d0cbbmsh6495b8b1beac76ep1b16e9jsn4956b21abca2', 'X-RapidAPI-Host': 'open-weather13.p.rapidapi.com'})

        # Test case 3: Empty location
        location = ""
        expected_output = "An error occurred: 'main'"
        
        forecast = get_weather_forecast(location)
        
        self.assertEqual(forecast, expected_output)

if __name__ == '__main__':
    unittest.main()
    