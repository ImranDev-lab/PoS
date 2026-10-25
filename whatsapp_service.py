"""WhatsApp delivery service. Integrate Twilio / WhatsApp Cloud API here."""


def send_invoice_whatsapp(invoice_id: str, phone: str, message: str = None) -> dict:
    # Placeholder: replace with Twilio Client or Meta WhatsApp Cloud API call
    return {
        "ok": True,
        "invoice_id": invoice_id,
        "to": phone,
        "message": message or f"Your invoice {invoice_id} is ready. Tap to pay/download PDF.",
        "provider": "placeholder",
        "note": "Add TWILIO_ACCOUNT_SID / TWILIO_AUTH_TOKEN or Meta WhatsApp Cloud API credentials",
    }