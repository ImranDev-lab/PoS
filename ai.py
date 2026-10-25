from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import AIStockPrediction, AILog
from ..services.voice import transcribe_and_parse
from ..services.ocr import extract_invoice_data
from ..services.ai_stock import predict_stock
import json

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/voice-to-bill")
async def voice_to_bill(file: UploadFile = File(...), db: Session = Depends(get_db)):
    audio = await file.read()
    text, items = await transcribe_and_parse(audio, file.filename or "audio.webm")
    log = AILog(
        action_type="voice_to_bill",
        input_data={"filename": file.filename},
        output_data={"text": text, "items": items},
    )
    db.add(log)
    db.commit()
    return {"transcription": text, "items": items}


@router.post("/ocr-invoice")
async def ocr_invoice(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    result = await extract_invoice_data(content, file.filename or "file")
    log = AILog(
        action_type="ocr_invoice",
        input_data={"filename": file.filename},
        output_data=result,
    )
    db.add(log)
    db.commit()
    return result


@router.post("/stock-prediction/{product_id}")
def stock_prediction(product_id: str, db: Session = Depends(get_db)):
    pred = predict_stock(db, product_id)
    if not pred:
        raise HTTPException(status_code=404, detail="Product not found or insufficient data")
    db.add(pred)
    db.commit()
    db.refresh(pred)
    return pred


@router.get("/stock-predictions")
def list_predictions(db: Session = Depends(get_db)):
    return db.query(AIStockPrediction).all()