from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.whatsapp_service import send_invoice_whatsapp

router = APIRouter()


class WhatsAppSend(BaseModel):
    invoice_id: str
    phone: str
    message: Optional[str] = None

    class Config:
        pass


from typing import Optional  # noqa: E402


@router.post("/send-invoice")
def send_invoice(payload: WhatsAppSend):
    result = send_invoice_whatsapp(payload.invoice_id, payload.phone, payload.message)
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result.get("error", "Failed to send"))
    return result