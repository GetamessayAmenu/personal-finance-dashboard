from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt_handler import get_current_user_with_db, create_access_token, get_current_user_from_cookie
import os

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User created successfully", "user": {"id": new_user.id, "username": new_user.username, "email": new_user.email}}

@router.post("/login")
def login(response: Response, user: schemas.UserLogin, db: Session = Depends(get_db)):
    """Login user and set httpOnly cookie"""
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create access token with user ID
    token_data = {"sub": db_user.email, "user_id": db_user.id}
    token = create_access_token(token_data)

    # Set httpOnly cookie
    response.set_cookie(
        key="access_token",
        value=token,
        max_age=1800,  # 30 minutes
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax"
    )

    return {"msg": "Login successful", "user": {"id": db_user.id, "username": db_user.username, "email": db_user.email}}

@router.post("/logout")
def logout(response: Response):
    """Logout user by clearing cookie"""
    response.delete_cookie(key="access_token")
    return {"msg": "Logout successful"}

@router.get("/me")
def get_current_user(user_data: dict = Depends(get_current_user_with_db)):
    """Get current user information"""
    return {
        "id": user_data["user_id"],
        "username": user_data.get("username", "Unknown"),
        "email": user_data["email"],
        "created_at": None  # We'll add this later if needed
    }