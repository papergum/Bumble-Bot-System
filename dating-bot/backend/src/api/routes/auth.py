"""
Authentication routes for the API.
This module provides endpoints for user authentication.
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from ..utils.response import success_response, error_response

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={401: {"description": "Unauthorized"}},
)

# Load configuration
config_path = Path(__file__).parent.parent.parent.parent / "config" / "api_config.json"
try:
    with open(config_path, "r") as f:
        config = json.load(f)
        security_config = config.get("security", {})
except (FileNotFoundError, json.JSONDecodeError) as e:
    logger.error(f"Failed to load API configuration: {e}")
    security_config = {
        "secret_key": "REPLACE_WITH_SECURE_SECRET_KEY",
        "algorithm": "HS256",
        "access_token_expire_minutes": 60
    }

# Security settings
SECRET_KEY = security_config.get("secret_key", "REPLACE_WITH_SECURE_SECRET_KEY")
ALGORITHM = security_config.get("algorithm", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = security_config.get("access_token_expire_minutes", 60)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# For demo purposes - in production, this would be a database
# This is a simple in-memory user store
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("admin"),
        "disabled": False
    }
}

def verify_password(plain_password, hashed_password):
    """
    Verify a password against a hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        bool: True if password matches hash
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    """
    Get a user from the database.
    
    Args:
        db: User database
        username: Username to look up
        
    Returns:
        UserInDB: User if found, None otherwise
    """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(fake_db, username: str, password: str):
    """
    Authenticate a user.
    
    Args:
        fake_db: User database
        username: Username to authenticate
        password: Password to verify
        
    Returns:
        UserInDB: User if authenticated, False otherwise
    """
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create an access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time
        
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get the current user from a token.
    
    Args:
        token: JWT token
        
    Returns:
        User: Current user
        
    Raises:
        HTTPException: If token is invalid
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Get the current active user.
    
    Args:
        current_user: Current user
        
    Returns:
        User: Current active user
        
    Raises:
        HTTPException: If user is disabled
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login to get an access token.
    
    Args:
        form_data: Form data with username and password
        
    Returns:
        Token: Access token
        
    Raises:
        HTTPException: If authentication fails
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        return error_response(
            message="Incorrect username or password",
            status_code=status.HTTP_401_UNAUTHORIZED,
            errors=[{"loc": ["form", "password"], "msg": "Invalid credentials"}]
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return success_response(
        data={"access_token": access_token, "token_type": "bearer"},
        message="Login successful"
    )

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get the current user.
    
    Args:
        current_user: Current user
        
    Returns:
        User: Current user
    """
    return success_response(
        data={"username": current_user.username},
        message="User details retrieved successfully"
    )

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_active_user)):
    """
    Logout the current user.
    
    Args:
        current_user: Current user
        
    Returns:
        Dict: Success message
    """
    # In a stateless JWT system, the client simply discards the token
    # Server-side we could implement a token blacklist for additional security
    return success_response(
        message="Logout successful"
    )