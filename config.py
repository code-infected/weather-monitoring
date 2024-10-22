import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
TEMP_THRESHOLD = float(os.getenv('TEMP_THRESHOLD', 35))
REQUEST_INTERVAL = 0.1 
