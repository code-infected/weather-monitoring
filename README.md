# Real-Time Weather Monitoring System

This is a real-time weather monitoring and data processing system designed to fetch weather data from the OpenWeatherMap API for multiple cities in India, process it, and store it in a PostgreSQL database. The application provides real-time weather updates, daily summaries, and threshold-based alerts. Data is visualized using **Streamlit** for user-friendly interaction.

## Features
- **Real-Time Weather Updates**: Fetches and stores weather data (temperature, main weather condition, etc.) from OpenWeatherMap API every 5 minutes.
- **Daily Weather Summaries**: Computes daily statistics such as average, max, and min temperatures, and the most frequent weather condition (rollups and aggregates).
- **Alerting Mechanism**: Generates alerts if weather conditions exceed predefined thresholds (e.g., temperature exceeds 35°C for two consecutive updates).
- **Visualization**: Displays real-time weather data, historical summaries, and alerts using Streamlit.
- **Extensible**: Designed to support more weather parameters like humidity, wind speed, and weather forecasts.

## Project Structure

```
weather_monitoring/
│
├── app/
│   ├── __init__.py               # Initialization file for the app package
│   ├── models.py                 # SQLAlchemy database models for weather data and summaries
│   ├── api.py                    # OpenWeatherMap API interaction and data storage
│   ├── data_processor.py         # Data rollups, aggregates, and alerting logic
│   ├── scheduler.py              # Task scheduler to periodically fetch data and run rollups
│   ├── visualizer.py             # Streamlit app for data visualization
│                  
│
├── tests/
│   ├── __init__.py               # Initialization file for the tests package
│   ├── test_app.py               # Test cases for weather data retrieval and processing
│
├── .env                          # Environment variables for API keys and database config
├── config.py                     # Configuration settings for API, cities, intervals, and DB
├── requirements.txt              # List of required Python packages
├── run_scheduler.py              # Script to run the scheduler
├── README.md                     # You are here
├── __init__.py                   # Initialization file for the tests subpackage

```

## Dependencies

The following dependencies are required to run the application:

### Python Dependencies
These are the main Python packages required to run the application, which are managed in the `requirements.txt` file.
- `requests`: For making HTTP requests to OpenWeatherMap API.
- `SQLAlchemy`: For working with PostgreSQL databases.
- `psycopg2-binary`: PostgreSQL adapter for Python.
- `schedule`: For scheduling periodic tasks like API calls.
- `streamlit`: For creating a dashboard to visualize weather data.

Install them using:

```bash
pip install -r requirements.txt
```

### PostgreSQL (Database)
The application uses PostgreSQL as the database to store both real-time weather data and daily summaries.

#### Using Docker for PostgreSQL:
You can use Docker to run PostgreSQL in a containerized environment.

1. **Download and run PostgreSQL container**:
   ```bash
   docker run --name weather-postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=weather_monitoring -p 5432:5432 -d postgres
   ```

2. **Verify connection**:
   You can verify the connection by running:
   ```bash
   docker exec -it weather-postgres psql -U postgres -d weather_monitoring
   ```

   The database URL will be used in `.env`:
   ```
   DATABASE_URL=postgresql://postgres:password@localhost/weather_monitoring
   ```

### Streamlit (Visualization)
Streamlit is used to create a simple UI for visualizing weather data.

To run the Streamlit app, use the following command:
```bash
streamlit run app/visualizer.py
```

### OpenWeatherMap API
The system uses the OpenWeatherMap API to fetch real-time weather data.

1. **Sign up** for an API key: https://openweathermap.org/appid
2. **Add the API key** to your `.env` file:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```

## Build Instructions

### 1. **Clone the Repository**
Clone the repository to your local machine:
```bash
git clone https://github.com/your-username/weather_monitoring.git
cd weather_monitoring
```

### 2. **Install Dependencies**
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. **Set Up PostgreSQL (Optional: Using Docker)**
If you don't have PostgreSQL installed locally, you can spin up a container with the following command:

```bash
docker run --name weather-postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=weather_monitoring -p 5432:5432 -d postgres
```

### 4. **Set Up Environment Variables**
Create a `.env` file in the root directory of the project and add the following environment variables:

```bash
OPENWEATHER_API_KEY=your_api_key_here
OPENWEATHER_API_KEY=postgresql://user:password@localhost:5432/weather_monitoring
DATABASE_URL=
SENDER_EMAIL = 
RECEIVER_EMAIL = 
EMAIL_PASSWORD = 
TEMP_THRESHOLD = 35 //default

```

### 5. **Run Migrations**
Ensure the database tables are created by running migrations using SQLAlchemy models:

```bash
python -c "from app.models import Base, engine; Base.metadata.create_all(bind=engine)"
```

### 6. **Run the Scheduler**
Run the task scheduler that will periodically fetch weather data from the OpenWeatherMap API and store it in the PostgreSQL database.

```bash
python run_scheduler.py
```

### 7. **Run the Streamlit Visualization**
Finally, start the Streamlit application to visualize real-time data and daily summaries.

```bash
streamlit run app/visualizer.py
```

## Design Choices

1. **Modular Design**: 
   - The project is broken down into modules, making it easy to maintain, extend, and test. For example, the `api.py` module is responsible for API interactions, `data_processor.py` handles processing and rollups, and `scheduler.py` manages periodic tasks.
   
2. **SQLAlchemy for ORM**: 
   - SQLAlchemy is used to map Python objects to PostgreSQL tables, ensuring that the interaction between Python code and the database is smooth and easy to extend.

3. **Task Scheduling with `schedule`**: 
   - The `schedule` package is used to run the periodic tasks such as fetching weather data from the OpenWeatherMap API every 5 minutes. It also ensures that daily summaries are computed at the end of the day.

4. **Streamlit for Visualization**:
   - Streamlit is an easy-to-use framework for creating real-time dashboards. It enables us to create a simple yet powerful user interface to view the current weather data, daily summaries, and alerts.

5. **Environment Variables**: 
   - Sensitive information like the API key and database connection details are stored in the `.env` file, which is not included in version control. This ensures security and flexibility when deploying the application in different environments.

6. **Error Handling**:
   - Basic error handling is implemented to ensure that failed API requests or database operations do not crash the system.

7. **Extensibility**: 
   - The system can easily be extended to support additional weather parameters such as wind speed, humidity, etc., and future functionality like weather forecasts can be incorporated.

## Running Tests

To ensure that the application works as expected, run the unit tests using:

```bash
python -m unittest discover tests
```


## License

This project is licensed under the MIT License.
