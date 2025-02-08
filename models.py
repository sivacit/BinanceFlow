from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BTCUSDT_1h_data(Base):
    __tablename__ = 'BTCUSDT_1h_data.csv'
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

# Add other fields based on your table structure
