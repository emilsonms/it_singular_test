from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.controllers.auth import ( 
UserCreateRequest, 
User, 
get_db, 
get_password_hash,
authenticate_user,
ACCESS_TOKEN_EXPIRE_MINUTES,
get_current_user,
verify_admin_role,
create_access_token)
from src.controllers.health import check_db_health
from datetime import timedelta
from src.schemas.auth import LoginRequest, Token




app = FastAPI()


@app.post("/token", response_model=Token)
async def login_for_access_token(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    data = {
        "id": user.id,
        "username": user.username,
        "role": user.role
    }

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": data.get("username")}, expires_delta=access_token_expires)
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": data
    }
    
@app.get("/user")
async def read_users_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"data": current_user}


@app.get("/admin")
async def read_admins_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_admin_role(current_user)
    return {"data": current_user}


@app.post("/create_user")
async def create_user(user: UserCreateRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    hashed_password = get_password_hash(user.password)
    
    new_user = User(username=user.username, password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"username": new_user.username, "role": new_user.role}


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    db_status = check_db_health(db)

    if db_status:
        return {"status": "ok", "database": "connected"}
    else:
        return {"status": "error", "database": "disconnected"}
