from sqlalchemy import func
from datetime import date, datetime, timedelta
from app.models import WeatherData, DailySummary, SessionLocal
from config import CITIES


def cleanup_old_data(days=30):
    session = SessionLocal()
    cutoff_date = datetime.now() - timedelta(days=days)
    session.query(WeatherData).filter(WeatherData.timestamp < cutoff_date).delete()
    session.commit()
    session.close()

# Function to calculate daily rollups
def calculate_daily_summary():
    session = SessionLocal()
    for city in CITIES:
        today = date.today()

        # Fetch today's weather data for the city
        data = session.query(WeatherData).filter(
            WeatherData.city == city,
            func.date(WeatherData.timestamp) == today
        ).all()

        if data:
            avg_temp = sum([entry.temperature for entry in data]) / len(data)  # Updated here
            max_temp = max([entry.temperature for entry in data])  # Updated here
            min_temp = min([entry.temperature for entry in data])  # Updated here

            # Find the most frequent weather condition
            condition_counts = {}
            for entry in data:
                condition_counts[entry.weather_main] = condition_counts.get(entry.weather_main, 0) + 1  # Updated here
            dominant_condition = max(condition_counts, key=condition_counts.get)

            # Save the daily summary
            daily_summary = DailySummary(
                city=city,
                date=today,
                avg_temp=avg_temp,
                max_temp=max_temp,
                min_temp=min_temp,
                dominant_weather=dominant_condition  # Updated here
            )
            session.add(daily_summary)
            session.commit()
    session.close()

# Function to monitor and alert on thresholds
def check_thresholds():
    session = SessionLocal()
    for city in CITIES:
        recent_data = session.query(WeatherData).filter(
            WeatherData.city == city
        ).order_by(WeatherData.timestamp.desc()).limit(2).all()

        if len(recent_data) == 2:
            if recent_data[0].temperature > 35 and recent_data[1].temperature > 35:  # Updated here
                print(f"ALERT: {city} temperature exceeded 35°C for two consecutive updates.")
                # Add logic for email alert (optional)
    session.close()
