from sqlalchemy.orm import Session
from sqlalchemy import text


def check_db_health(db: Session):
    try:
        db.execute(text("SELECT 1"))
        return True
    
    except Exception:
        return False
