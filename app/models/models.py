from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String(255), nullable=False)
    password = Column(String)
    rol = Column(String)
    token = Column(String(255), nullable=True)
    events = relationship("Event", back_populates="owner")

    
class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    capacity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    event_date = Column(DateTime)
    address = Column(String)
    status = Column(String, default="Pendiente")  
    owner_id = Column(Integer, ForeignKey('users.id'))
    attendees = relationship("Attendee", back_populates="event")
    speakers = relationship("Speaker", back_populates="event", cascade="all, delete-orphan")

class Attendee(Base):
    __tablename__ = 'attendees'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    created_at = Column(DateTime, default=datetime.utcnow)  # Ajuste aquí
    # Relación con Event
    event = relationship("Event", back_populates="attendees")

class Speaker(Base):
    __tablename__ = 'speakers'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    description = Column(Text, nullable=True)   
    # Relación con el modelo Event
    event = relationship("Event", back_populates="speakers")


# Definir relaciones después de las clases
User.events = relationship("Event", back_populates="owner")
Event.owner = relationship("User", back_populates="events")
