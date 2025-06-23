from fastapi import APIRouter, Depends, HTTPException , Header
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas
from auth.firebase import verify_firebase_token

router = APIRouter(prefix="/users", tags=["users"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/get_role")
def get_role(authorization: str = Header(...), db: Session = Depends(get_db)):
    # Expecting header: Authorization: Bearer <firebase_token>
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    decoded = verify_firebase_token(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")
    email = decoded.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email not found in token")
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if not db_user or not db_user.role:
        raise HTTPException(status_code=404, detail="User or role not found")
    return {"role": db_user.role.name,"id": db_user.id }

@router.post("/login", response_model=schemas.UserLoginResponse)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
        "role": db_user.role.name if db_user.role else None
    }



@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(user.model_dump())
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=list[schemas.User])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).get(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")
    for key, value in user.model_dump().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    db.delete(user)
    db.commit()
    return {"ok": True}


