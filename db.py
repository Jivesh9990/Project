import sqlalchemy
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# setup code
Base = declarative_base()

# class for table
class Setting(Base):
    __tablename__ ='settings'
    id = Column(Integer, primary_key=True)
    window_width = Column(Integer, default=640)
    window_height = Column(Integer, default=480)
    window_name = Column(String,default='video_window')
    modified_on = Column(DateTime, default=datetime.now)

# code to create db
if __name__ == "__main__":
    engine = create_engine('sqlite:///db.sqlite3')
    Base.metadata.create_all(engine)