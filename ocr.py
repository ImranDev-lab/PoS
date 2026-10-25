"""Invoice OCR service. Plug in PyTesseract/EasyOCR or OpenAI Vision here."""
from typing import Any


async def extract_invoice_data(content: bytes, filename: str) -> dict[str, Any]:
    # Placeholder: integrate pytesseract / easyocr / OpenAI Vision for real extraction
    return {
        "vendor_name": "Extracted Vendor",
        "invoice_number": "EXT-001",
        "date": "2026-10-25",
        "items": [{"name": "Sample Item", "quantity": 1, "cost_price": 100.0}],
        "total": 100.0,
        "note": "OCR integration pending: plug in pytesseract/easyocr/OpenAI Vision",
    }