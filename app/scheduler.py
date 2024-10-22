import schedule
import time
from app.api import fetch_weather_data
from app.data_processor import calculate_daily_summary, check_thresholds
from config import REQUEST_INTERVAL

# Function to schedule tasks
def schedule_tasks():
    schedule.every(REQUEST_INTERVAL).minutes.do(fetch_weather_data)
    schedule.every().day.at("23:59").do(calculate_daily_summary)
    schedule.every(REQUEST_INTERVAL).minutes.do(check_thresholds)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    schedule_tasks()
