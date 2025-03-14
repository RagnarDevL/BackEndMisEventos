# app/schemas.py
from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime 
from sqlalchemy.orm import relationship, registry

# Crea una instancia del registrador
mapper_registry = registry()

# Define tu modelo base
Base = mapper_registry.generate_base()

class Token(BaseModel):
    token: str


class Login(BaseModel):
    username: str
    password: str
    
class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    email: str
    password: str
    rol: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class SessionBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    capacity: int

class SessionCreate(SessionBase):
    pass

class SessionUpdate(SessionBase):
    pass

class Session(SessionBase):
    id: int

    class Config:
        orm_mode = True

class Attendee(BaseModel):
    id: int
    name: str
    email: str
    event_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Attendee(BaseModel):
    id: int
    name: str
    email: str
    event_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class Event(BaseModel):
    id: int
    name: str
    capacity: int
    created_at: datetime
    event_date: datetime
    address: str
    status: str  # Agrega el campo status aquí
    attendees: List[Attendee] = []

    class Config:
        orm_mode = True
    

class EventResponse(BaseModel):
    id: int
    name: str
    capacity: int
    created_at: datetime
    event_date: datetime
    address: str
    attendees: int
    status: str
    class Config:
        orm_mode = True


class EventCreate(BaseModel):
    name: str
    capacity: int
    event_date: datetime
    address: str
    status: str = "Pendiente"

    class Config:
        orm_mode = True

class EventUpdate(BaseModel):
    name: str
    capacity: int
    event_date: datetime  
    address: str
    status: str
    class Config:
        orm_mode = True

class AttendeeCreate(BaseModel):
    name: str
    email: str

class SpeakerBase(BaseModel):
    name: str
    event_id: int
    description: Optional[str] = ""

class SpeakerCreate(SpeakerBase):
    pass  # Puedes agregar validaciones adicionales si es necesario

class Speaker(SpeakerBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  
# Llama a configure() para aplicar las configuraciones
mapper_registry.configure()