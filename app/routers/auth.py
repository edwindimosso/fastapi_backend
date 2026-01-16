from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import schemas, models, utils
from .. import database



router = APIRouter(

    tags=["Authentication"]
)

@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user= db.query(models.UserModel).filter(models.UserModel.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_FORBIDDEN, detail="Invalid Credentials")
 
    return "example token"
