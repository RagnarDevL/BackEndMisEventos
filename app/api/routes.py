from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from app.db.database import SessionLocal
from app.models.models import User as UserModel, Event as EventModel, Attendee as AttendeeModel,Speaker as SpeakerModel
from app.schemas import SpeakerBase
from app.schemas import EventCreate, EventUpdate, Event, Login, Attendee, AttendeeCreate, EventResponse,UserCreate,UserBase
from app.utils import get_current_user, get_db, authenticate_user, create_access_token, get_current_user2,hash_password
from datetime import datetime, timedelta
from typing import List
from datetime import datetime
from sqlalchemy import desc


router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear un nuevo usuario
@router.post("/userCreate/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    new_user = UserModel(email=user.email,name=user.name, password=hashed_password, rol=user.rol)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# Crear un nuevo evento
@router.post("/events/", response_model=Event)
def create_event(event: EventCreate, db: Session = Depends(get_db),token: str = Query(...)):
    print("ENTRAAAA CREAR EVENTO")
    current_user = get_current_user2(token, db)
    db_event = EventModel(**event.dict(), owner_id=current_user.id, created_at=datetime.now())  # Agrega created_at aquí
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

# Leer todos los eventos
@router.get("/events/", response_model=list[Event])
def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    events = db.query(EventModel).offset(skip).limit(limit).all()  # Usa EventModel aquí
    return events

# Leer todos los eventos del usuario logueado
@router.get("/eventsByUser", response_model=List[EventResponse])
async def read_events(
    db: Session = Depends(get_db),
    search: str='',
    token: str = Query(...),  # Recibe el token como un parámetro de consulta
):
    try:
        current_user = get_current_user2(token, db)
        if not current_user:
            raise HTTPException(status_code=401, detail="Invalid token")

        if(current_user.rol == "Asistente"):
            events = db.query(EventModel).options(joinedload(EventModel.attendees)) \
            .filter(EventModel.name.ilike(f"{search}%")) \
            .order_by(desc(EventModel.id)) \
            .all()
        else:
            events = db.query(EventModel).options(joinedload(EventModel.attendees)) \
            .filter(EventModel.owner_id == current_user.id,EventModel.name.ilike(f"{search}%")) \
            .order_by(desc(EventModel.id)) \
            .all()
        
        
        event_responses = []
        for event in events:
            attendee_count = db.query(AttendeeModel).filter(AttendeeModel.event_id == event.id).count()
            
            event_response = {
                "id": event.id,
                "name": event.name,
                "capacity": event.capacity,
                "created_at": event.created_at,
                "event_date": event.event_date,
                "address": event.address,
                "attendees": attendee_count,
                "status": event.status
            }
            

            event_responses.append(event_response)
        
        return event_responses
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Leer un evento por ID
@router.get("/events/{event_id}", response_model=Event)
def read_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(EventModel).filter(EventModel.id == event_id).first()  # Usa EventModel aquí
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# Actualizar un evento
@router.put("/events/{event_id}", response_model=Event)
def update_event(event_id: int, event: EventUpdate, db: Session = Depends(get_db),token: str = Query(...)):
    db_event = db.query(EventModel).filter(EventModel.id == event_id).first()  # Usa EventModel aquí
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    for key, value in event.dict().items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event

# Eliminar un evento
@router.delete("/events/{event_id}", response_model=Event)
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_event = db.query(EventModel).filter(EventModel.id == event_id).first()  # Usa EventModel aquí
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(db_event)
    db.commit()
    return db_event

# IniciarSesion
@router.post("/login")
async def login(login: Login, db: Session = Depends(get_db)):
    user = authenticate_user(db, login.username, login.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=150)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    # Obtener la fecha y hora actual
    now = datetime.utcnow()
    # Actualizar el estado de los eventos que han vencid
    db.query(EventModel).filter(EventModel.event_date < now).update({EventModel.status: "Vencido"}, synchronize_session=False)     
    # Confirmar los cambios en la base de datos
    db.commit()
    return {"access_token": access_token, "token_type": "bearer","rol": user.rol,"Nombre": user.name,"Email": user.email}

# Agregar un asistente al evento
@router.post("/events/{event_id}/attendees", response_model=Attendee)
def add_attendee_to_event(
    event_id: int,
    attendee: AttendeeCreate,
    db: Session = Depends(get_db),
):
    return create_attendee_for_event(db, event_id, attendee)

def create_attendee_for_event(db: Session, event_id: int, attendee_data: AttendeeCreate):
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    print("ANTES DE ")
    attendees = db.query(AttendeeModel).filter(
        AttendeeModel.email == attendee_data.email,
        AttendeeModel.event_id == event_id  
    ).first()
    if attendees:
        raise HTTPException(status_code=400, detail="YA TE ENCUENTRAS REGISTRADO EN ESTE EVENTO")
    new_attendee = AttendeeModel(**attendee_data.dict(), event_id=event_id)
    db.add(new_attendee)
    db.commit()
    db.refresh(new_attendee)
    return new_attendee

# Obtener asistentes al evento
@router.get("/events/{event_id}/attendeesByEvent", response_model=List[Attendee])
def get_attendees_by_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    attendees = db.query(AttendeeModel).filter(AttendeeModel.event_id == event_id).all()
    return attendees

# Leer todos los eventos del usuario logueado
@router.get("/eventsMyRegister", response_model=List[EventResponse])
async def read_events(
    db: Session = Depends(get_db),
    token: str = Query(...),  # Recibe el token como un parámetro de consulta
):
    try:
        current_user = get_current_user2(token, db)
        if not current_user:
            raise HTTPException(status_code=401, detail="Invalid token")
        event_filter = []
        attendees = db.query(AttendeeModel).filter(AttendeeModel.email == current_user.email).all()
        for attend in attendees:
            events = db.query(EventModel).options(joinedload(EventModel.attendees)).filter(EventModel.id == attend.event_id).all()
            
            for event in events:
                event_filter.append(event)  
        
        event_responses = []
        for event in event_filter:
            print("ENTRAAA",event)
            attendee_count = db.query(AttendeeModel).filter(AttendeeModel.event_id == event.id).count()
            
            event_response = {
                "id": event.id,
                "name": event.name,
                "capacity": event.capacity,
                "created_at": event.created_at,
                "event_date": event.event_date,
                "address": event.address,
                "attendees": attendee_count,
                "status": event.status
            }
            

            event_responses.append(event_response)
        
        return event_responses
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Crear un ponente 
@router.post("/speakers/", response_model=SpeakerBase)
def create_speaker(speaker: SpeakerBase, db: Session = Depends(get_db)):
    db_speaker = SpeakerModel(**speaker.dict())
    db.add(db_speaker)
    db.commit()
    db.refresh(db_speaker)
    return db_speaker

# Obtener los ponentes de un evento
@router.get("/speakers/{event_id}", response_model=List[SpeakerBase])
def list_speakers(event_id: int, db: Session = Depends(get_db)):
    speakers = db.query(SpeakerModel).filter(SpeakerModel.event_id == event_id).all()
    if not speakers:
        raise HTTPException(status_code=404, detail="No speakers found for this event")
    print(speakers)  # Verifica qué datos se están recuperando
    return speakers

