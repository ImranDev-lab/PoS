from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..services.sync_service import get_pending_sync, apply_offline_changes

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/pending")
def pending_sync(db: Session = Depends(get_db)):
    return get_pending_sync(db)


@router.post("/bulk")
def bulk_sync(payload: list, db: Session = Depends(get_db)):
    return apply_offline_changes(db, payload)