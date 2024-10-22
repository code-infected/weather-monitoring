from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATABASE_URL

Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(100), nullable=False, index=True)
    temperature = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    weather_main = Column(String(50), nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    humidity = Column(Float, nullable=True) 
    pressure = Column(Float)  # Make sure this line exists
    wind_speed = Column(Float, nullable=True) 

    def __repr__(self):
        return f"<WeatherData(city='{self.city}', temp={self.temperature}°C, time={self.timestamp})>"

class DailySummary(Base):
    __tablename__ = 'daily_summary'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(100), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    avg_temp = Column(Float, nullable=False)
    max_temp = Column(Float, nullable=False)
    min_temp = Column(Float, nullable=False)
    humidity = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True) 
    dominant_weather = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<DailySummary(city='{self.city}', date={self.date.date()}, avg_temp={self.avg_temp}°C)>"

def init_db():
    """Initialize database connection and create tables."""
    if DATABASE_URL is None:
        raise ValueError("DATABASE_URL is not set in the environment variables")
    
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return engine, SessionLocal

# Initialize database connection
engine, SessionLocal = init_db()

def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AlertConfig(Base):
    __tablename__ = 'alert_configs'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False)
    temp_threshold = Column(Float, nullable=False)
    consecutive_readings = Column(Integer, default=2)
    created_at = Column(DateTime, default=datetime)
    updated_at = Column(DateTime, default=datetime, onupdate=datetime)

class WeatherAlert(Base):
    __tablename__ = 'weather_alerts'
    
    id = Column(Integer, primary_key=True)
    city = Column(String(50), nullable=False)
    alert_type = Column(String(50), nullable=False)
    message = Column(String(200), nullable=False)
    temperature = Column(Float)
    consecutive_count = Column(Integer)
    timestamp = Column(DateTime, default=datetime)
