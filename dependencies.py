from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User
from auth import verify_access_token

# JWT Token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# ----------------------------
# Database Dependency
# ----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------
# Get Current Logged-in User
# ----------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    email = verify_access_token(token)

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Expired Token"
        )

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Not Found"
        )

    return user


# ----------------------------
# Admin Only
# ----------------------------
def admin_only(
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin Access Required"
        )

    return current_user


# ----------------------------
# Employee Only
# ----------------------------
def employee_only(
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "Employee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Employee Access Required"
        )

    return current_user


# ----------------------------
# IT Support Only
# ----------------------------
def support_only(
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "IT Support":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="IT Support Access Required"
        )

    return current_user