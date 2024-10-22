import streamlit as st
import requests
from sqlalchemy.orm import sessionmaker
from models import WeatherData, DailySummary, engine, WeatherAlert
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Weather icon mapping
def get_weather_icon(condition):
    """Map weather conditions to appropriate OpenWeatherMap icon codes"""
    icon_mapping = {
        'Clear': '01d',
        'Clouds': '03d',
        'Few clouds': '02d',
        'Scattered clouds': '03d',
        'Broken clouds': '04d',
        'Shower rain': '09d',
        'Rain': '10d',
        'Thunderstorm': '11d',
        'Snow': '13d',
        'Mist': '50d',
        'Fog': '50d',
        'Haze': '50d',
        'Smoke': '50d',
        'Dust': '50d',
        'Sand': '50d',
        'Drizzle': '09d',
        # Add night versions
        'Clear night': '01n',
        'Few clouds night': '02n',
        'Scattered clouds night': '03n',
        'Broken clouds night': '04n',
        'Shower rain night': '09n',
        'Rain night': '10n',
        'Thunderstorm night': '11n',
        'Snow night': '13n',
        'Mist night': '50n'
    }
    return icon_mapping.get(condition, '01d')  # Default to clear sky if condition not found

def get_weather_icon_url(condition):
    """Get the full URL for the weather icon based on the condition"""
    icon_code = get_weather_icon(condition)
    return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

# Page configuration
st.set_page_config(
    page_title="Weather Monitoring System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with dark theme
st.markdown("""
    <style>
    .main {
        background-color: #1a1a1a;
        padding: 2rem;
    }
    .weather-card {
        background-color: #2d2d2d;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        margin-bottom: 1rem;
        color: #ffffff;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #3498db;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #bababa;
    }
    h1, h2, h3, h4 {
        color: #ffffff !important;
    }
    .stSelectbox label {
        color: #ffffff !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    .plot-container {
        background-color: #2d2d2d;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
    }
    .sidebar .sidebar-content {
        background-color: #1a1a1a;
    }
    .sidebar .widget-label {
        color: #ffffff !important;
    }
    .stAlert {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    .stDataFrame {
        background-color: #2d2d2d;
    }
    .stDataFrame td {
        color: #ffffff !important;
    }
    .stDataFrame th {
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize database session
Session = sessionmaker(bind=engine)
session = Session()

def convert_temperature(temp, unit):
    if unit == 'Fahrenheit':
        return (temp * 9/5) + 32
    return temp

# Title
st.markdown("<h1 style='text-align: center; color: #ffffff;'>🌤️ Weather Monitoring System</h1>", unsafe_allow_html=True)

# Temperature unit selection
temp_unit = st.selectbox("Select Temperature Unit", options=['Celsius', 'Fahrenheit'], index=0)

# City selection with "All" option
st.markdown("<br>", unsafe_allow_html=True)
city = st.selectbox(
    "Select City",
    options=['All', 'Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad'],
    index=0
)

# Alert Configuration Section
st.sidebar.markdown("### Alert Configuration")
temp_threshold = st.sidebar.number_input("Temperature Threshold (°C)", min_value=0.0, max_value=50.0, value=35.0)
consecutive_updates = st.sidebar.number_input("Consecutive Updates for Alert", min_value=1, value=2)
enable_alerts = st.sidebar.checkbox("Enable Temperature Alerts", value=True)

# Date Range Selection
st.sidebar.markdown("### Date Range")
days_to_show = st.sidebar.slider("Days of Historical Data", min_value=1, max_value=30, value=7)

# Create two columns for layout
col1, col2 = st.columns(2)

# Current Weather Card
with col1:
    st.markdown("<h3>Current Weather</h3>", unsafe_allow_html=True)
    if city == 'All':
        recent_weather_list = []
        for city_name in ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']:
            weather = session.query(WeatherData).filter(
                WeatherData.city == city_name
            ).order_by(WeatherData.timestamp.desc()).first()
            if weather:
                recent_weather_list.append(weather)
    else:
        recent_weather = session.query(WeatherData).filter(
            WeatherData.city == city
        ).order_by(WeatherData.timestamp.desc()).first()
        recent_weather_list = [recent_weather] if recent_weather else []

    for recent_weather in recent_weather_list:
        if recent_weather:
            # Use the new weather icon mapping function
            icon_url = get_weather_icon_url(recent_weather.weather_main)
            temp_value = convert_temperature(recent_weather.temperature, temp_unit)
            feels_like_value = convert_temperature(recent_weather.feels_like, temp_unit)
            
            with st.container():
                st.markdown(f"""
                <div class="weather-card">
                    <h4>{recent_weather.city}</h4>
                    <img src="{icon_url}" style="float: right; margin: -20px -10px 0 0;">
                    <div class="metric-value">{temp_value:.1f}°{temp_unit[0]}</div>
                    <div class="metric-label">{recent_weather.weather_main}</div>
                    <br>
                    <div style="color: #ffffff;">
                        Feels Like: {feels_like_value:.1f}°{temp_unit[0]}<br>
                        Humidity: {recent_weather.humidity}%<br>
                        Wind Speed: {recent_weather.wind_speed} m/s
                    </div>
                    <div style="color: #bababa; font-size: 0.8rem;">
                        Last Updated: {recent_weather.timestamp.strftime('%I:%M %p, %b %d')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error(f"No recent data available for {city}")

# Daily Summary Card
with col2:
    st.markdown("<h3>Daily Summary</h3>", unsafe_allow_html=True)
    
    if city == 'All':
        summary_list = []
        for city_name in ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']:
            summary = session.query(DailySummary).filter(
                DailySummary.city == city_name
            ).order_by(DailySummary.date.desc()).first()
            if summary:
                summary_list.append(summary)
    else:
        daily_summary = session.query(DailySummary).filter(
            DailySummary.city == city
        ).order_by(DailySummary.date.desc()).first()
        summary_list = [daily_summary] if daily_summary else []

    for daily_summary in summary_list:
        if daily_summary:
            max_temp = convert_temperature(daily_summary.max_temp, temp_unit)
            min_temp = convert_temperature(daily_summary.min_temp, temp_unit)
            avg_temp = convert_temperature(daily_summary.avg_temp, temp_unit)
            
            with st.container():
                st.markdown(f"""
                <div class="weather-card">
                    <h4>{daily_summary.city}</h4>
                    <h4>Temperature Range</h4>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                        <div>
                            <div class="metric-value" style="color: #e74c3c;">{max_temp:.1f}°{temp_unit[0]}</div>
                            <div class="metric-label">Maximum</div>
                        </div>
                        <div>
                            <div class="metric-value" style="color: #3498db;">{min_temp:.1f}°{temp_unit[0]}</div>
                            <div class="metric-label">Minimum</div>
                        </div>
                    </div>
                    <div>
                        <h4>Average Temperature</h4>
                        <div class="metric-value" style="font-size: 1.5rem;">{avg_temp:.1f}°{temp_unit[0]}</div>
                    </div>
                    <div style="margin-top: 1rem;">
                        <div class="metric-label">Dominant Condition</div>
                        <div style="font-size: 1.2rem; color: #ffffff;">{daily_summary.dominant_condition}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error(f"No summary data available for {city}")

# Alert Section
st.markdown("<h3>Weather Alerts</h3>", unsafe_allow_html=True)
if enable_alerts:
    if city == 'All':
        alerts = session.query(WeatherAlert).filter(
            WeatherAlert.temperature >= temp_threshold
        ).order_by(WeatherAlert.timestamp.desc()).limit(5).all()
    else:
        alerts = session.query(WeatherAlert).filter(
            WeatherAlert.city == city,
            WeatherAlert.temperature >= temp_threshold
        ).order_by(WeatherAlert.timestamp.desc()).limit(5).all()
    
    if alerts:
        for alert in alerts:
            st.warning(f"""
                🚨 Temperature Alert for {alert.city}
                Temperature: {convert_temperature(alert.temperature, temp_unit):.1f}°{temp_unit[0]}
                Time: {alert.timestamp.strftime('%I:%M %p, %b %d')}
            """)
    else:
        st.info("No active temperature alerts")

# Enhanced Data Visualization Section
st.markdown("<h3>Weather Analysis</h3>", unsafe_allow_html=True)

# Fetch historical data based on selected days
historical_start = datetime.now() - timedelta(days=days_to_show)

if city == 'All':
    historical_data = session.query(WeatherData).filter(
        WeatherData.timestamp >= historical_start
    ).order_by(WeatherData.timestamp.asc()).all()
else:
    historical_data = session.query(WeatherData).filter(
        WeatherData.city == city,
        WeatherData.timestamp >= historical_start
    ).order_by(WeatherData.timestamp.asc()).all()

if historical_data:
    df = pd.DataFrame([{
        'timestamp': data.timestamp,
        'temperature': convert_temperature(data.temperature, temp_unit),
        'humidity': data.humidity,
        'pressure': data.pressure,
        'feels_like': convert_temperature(data.feels_like, temp_unit),
        'wind_speed': data.wind_speed,
        'city': data.city
    } for data in historical_data])
    
    # Temperature Trend
    fig_temp = go.Figure()
    
    if city == 'All':
        for city_name in df['city'].unique():
            city_data = df[df['city'] == city_name]
            fig_temp.add_trace(go.Scatter(
                x=city_data['timestamp'],
                y=city_data['temperature'],
                name=f'{city_name} Temperature',
                line=dict(width=2)
            ))
    else:
        fig_temp.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['temperature'],
            name='Temperature',
            line=dict(color='#3498db', width=2)
        ))
        fig_temp.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['feels_like'],
            name='Feels Like',
            line=dict(color='#e74c3c', width=2, dash='dash')
        ))
    
    fig_temp.update_layout(
        title=f'Temperature Trends (Last {days_to_show} Days)',
        paper_bgcolor='#2d2d2d',
        plot_bgcolor='#2d2d2d',
        font=dict(color='#ffffff'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#404040',
            title='Date'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#404040',
            title=f'Temperature (°{temp_unit[0]})'
        ),
        legend=dict(
            bgcolor='#2d2d2d',
            bordercolor='#404040'
        )
    )
    
    st.plotly_chart(fig_temp, use_container_width=True)
    
    # Additional visualizations
    col3, col4 = st.columns(2)
    
    with col3:
        fig_humidity = px.line(df, x='timestamp', y='humidity', 
                             color='city' if city == 'All' else None,
                             title=f'Humidity Trends (Last {days_to_show} Days)')
        fig_humidity.update_layout(
            paper_bgcolor='#2d2d2d',
            plot_bgcolor='#2d2d2d',
            font=dict(color='#ffffff'),
            xaxis=dict(showgrid=True, gridcolor='#404040'),
            yaxis=dict(showgrid=True, gridcolor='#404040', title='Humidity (%)')
        )
        st.plotly_chart(fig_humidity, use_container_width=True)
    
    with col4:
        fig_wind = px.line(df, x='timestamp', y='wind_speed', 
                          color='city' if city == 'All' else None,
                          title=f'Wind Speed Trends (Last {days_to_show} Days)')
        fig_wind.update_layout(
            paper_bgcolor='#2d2d2d',
            plot_bgcolor='#2d2d2d',
            font=dict(color='#ffffff'),
            xaxis=dict(showgrid=True, gridcolor='#404040'),
            yaxis=dict(showgrid=True, gridcolor='#404040', title='Wind Speed (m/s)')
        )
        st.plotly_chart(fig_wind, use_container_width=True)

    # Daily Statistics Table
    st.markdown("<h3>Daily Statistics</h3>", unsafe_allow_html=True)
    daily_stats = df.groupby(['city', df['timestamp'].dt.date]).agg({
        'temperature': ['mean', 'min', 'max'],
        'humidity': 'mean',
        'wind_speed': 'mean'
    }).round(2)
    
    daily_stats.columns = ['Avg Temp', 'Min Temp', 'Max Temp', 'Avg Humidity', 'Avg Wind Speed']
    daily_stats = daily_stats.reset_index()
    
    st.dataframe(daily_stats, use_container_width=True)

else:
    st.error("No historical data available for visualization")

# Footer with last update time
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align: center; color: #bababa;'>Last updated: {datetime.now().strftime('%I:%M %p, %b %d, %Y')}</div>", unsafe_allow_html=True)

session.close()