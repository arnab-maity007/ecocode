"""
Authentication and user management router (optional).
Provides endpoints for user registration, login, and JWT token management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import crud, schemas
from ..database import get_db
from ..utils.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)
from ..config import settings

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

# OAuth2 password bearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Dependency to get the current authenticated user from JWT token.
    
    Args:
        token: JWT token from Authorization header
        db: Database session
    
    Returns:
        User model instance
    
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = decode_access_token(token)
    if username is None:
        raise credentials_exception
    
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    
    return user


@router.post("/register", response_model=schemas.UserResponse, status_code=201)
async def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.
    
    **Request Body:**
    ```json
    {
        "email": "user@example.com",
        "username": "johndoe",
        "password": "securepassword123"
    }
    ```
    
    **Returns:**
    Created user details (without password).
    
    **Errors:**
    - 400: Email or username already registered
    """
    # Check if email already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Check if username already exists
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )
    
    # Hash password and create user
    hashed_password = get_password_hash(user.password)
    created_user = crud.create_user(db, user=user, hashed_password=hashed_password)
    
    return created_user


@router.post("/login", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login with username and password to get JWT token.
    
    **Form Data:**
    - username: User's username
    - password: User's password
    
    **Returns:**
    ```json
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer"
    }
    ```
    
    **Usage:**
    Include the token in subsequent requests:
    ```
    Authorization: Bearer <access_token>
    ```
    
    **Errors:**
    - 401: Invalid username or password
    """
    # Authenticate user
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user account"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
async def get_current_user_info(
    current_user = Depends(get_current_user)
):
    """
    Get current authenticated user's information.
    
    **Headers:**
    ```
    Authorization: Bearer <access_token>
    ```
    
    **Returns:**
    Current user details.
    
    **Errors:**
    - 401: Invalid or expired token
    """
    return current_user


@router.get("/users", response_model=list[schemas.UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all users (admin only feature - can be extended).
    
    **Query Parameters:**
    - skip: Pagination offset
    - limit: Maximum results
    
    **Returns:**
    List of users.
    
    **Note:** In production, restrict this to admin users only.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
