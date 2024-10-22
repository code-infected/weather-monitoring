import unittest
from app.api import get_weather_data

class TestWeatherData(unittest.TestCase):
    def test_weather_data_retrieval(self):
        city = "Delhi"
        data = get_weather_data(city)
        self.assertIn("city", data)
        self.assertEqual(data['city'], city)

if __name__ == '__main__':
    unittest.main()
