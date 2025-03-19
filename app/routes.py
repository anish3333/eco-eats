from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from . import models, schemas, database

router = APIRouter()

# Get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new user
@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, phone_no=user.phone_no, address=user.address)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Get users by optional name filter
@router.get("/users/search", response_model=list[schemas.UserResponse])
def read_users(name: str = Query(None), db: Session = Depends(get_db)):
    query = db.query(models.User)
    if name:
        query = query.filter(models.User.name == name)
    return query.all()


# Read user by ID
@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update user details
@router.put("/users/{user_id}")
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.phone_no = user.phone_no
    db_user.address = user.address
    db.commit()
    db.refresh(db_user)
    return {"message": "User updated successfully"}


# Delete user by ID
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
