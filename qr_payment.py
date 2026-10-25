import os
import qrcode


def generate_qr_payload(invoice_id: str, amount: float, merchant: str = "RetailMerchant") -> str:
    return f"pospay://pay?invoice_id={invoice_id}&amount={amount}&merchant={merchant}"


def generate_qr_image(invoice_id: str, amount: float) -> str:
    os.makedirs("static/qr", exist_ok=True)
    payload = generate_qr_payload(invoice_id, amount)
    img = qrcode.make(payload)
    filename = f"qr_{invoice_id}.png"
    path = os.path.join("static/qr", filename)
    img.save(path)
    return path