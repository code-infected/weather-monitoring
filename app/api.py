import requests
from datetime import datetime
import logging
from app.models import WeatherData, SessionLocal
import config
from typing import Dict, Any
from requests.exceptions import RequestException
from sqlalchemy.exc import SQLAlchemyError

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_weather_data(city: str) -> Dict[str, Any]:
    """
    Fetch weather data for a specific city from OpenWeatherMap API
    
    Args:
        city (str): Name of the city
    
    Returns:
        Dict[str, Any]: Dictionary containing weather data
    """
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        logger.info(f"Successfully fetched weather data for {city}")
        
        # Only return the fields that exist in your WeatherData model
        return {
            'city': city,
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'weather_main': data['weather'][0]['main'],
            'timestamp': datetime.fromtimestamp(data['dt'])
        }
    
    except RequestException as e:
        logger.error(f"Failed to fetch weather data for {city}: {str(e)}")
        raise
    except KeyError as e:
        logger.error(f"Missing required data in API response for {city}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while fetching weather data for {city}: {str(e)}")
        raise

def save_weather_data(weather_data: Dict[str, Any]) -> None:
    """
    Save weather data to database
    
    Args:
        weather_data (Dict[str, Any]): Dictionary containing weather data
    """
    session = SessionLocal()
    try:
        weather_entry = WeatherData(
            city=weather_data['city'],
            temperature=weather_data['temperature'],
            feels_like=weather_data['feels_like'],
            humidity=weather_data['humidity'],
            wind_speed=weather_data['wind_speed'],
            weather_main=weather_data['weather_main'],
            timestamp=weather_data['timestamp']
        )
        
        session.add(weather_entry)
        session.commit()
        logger.info(f"Successfully saved weather data for {weather_data['city']}")
    
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error while saving weather data for {weather_data['city']}: {str(e)}")
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Unexpected error while saving weather data for {weather_data['city']}: {str(e)}")
        raise
    finally:
        session.close()

def fetch_weather_data() -> None:
    """
    Fetch and save weather data for all configured cities
    """
    successful_cities = []
    failed_cities = []
    
    for city in config.CITIES:
        try:
            logger.info(f"Starting weather data fetch for {city}")
            weather_data = get_weather_data(city)
            save_weather_data(weather_data)
            successful_cities.append(city)
            logger.info(f"Successfully processed weather data for {city}")
        
        except Exception as e:
            logger.error(f"Failed to process weather data for {city}: {str(e)}")
            failed_cities.append(city)
    
    # Log summary
    logger.info(f"Weather data fetch completed. Successful: {len(successful_cities)}, Failed: {len(failed_cities)}")
    if failed_cities:
        logger.warning(f"Failed cities: {', '.join(failed_cities)}")

if __name__ == "__main__":
    fetch_weather_data()