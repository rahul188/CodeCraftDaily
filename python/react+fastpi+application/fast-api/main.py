from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Secret key to sign JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Fake user database for demonstration purposes
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "hashed_password": "fakehashedpassword",
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

# Function to create JWT token
def create_jwt_token(data: dict):
    to_encode = data.copy()
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Function to get the current user from JWT token
def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
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
    except JWTError:
        raise credentials_exception
    return username

# Route to create JWT token (login)
@app.post("/token", response_model=Token)
def login_for_access_token(form_data: User):
    user = fake_users_db.get(form_data.username)
    if user and form_data.password == "fakepassword":
        token_data = {"sub": form_data.username}
        return {"access_token": create_jwt_token(token_data), "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

# Example protected route
@app.get("/users/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
