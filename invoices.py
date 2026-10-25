import os
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..deps import get_current_user
from ..models import Invoice, InvoiceItem, Product
from ..schemas import InvoiceCreate, InvoiceOut
from ..services.invoice_pdf import generate_invoice_pdf

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=InvoiceOut)
def create_invoice(
    payload: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    invoice_number = f"INV-{uuid.uuid4().hex[:10].upper()}"
    subtotal = sum(float(i.unit_price) * float(i.quantity) for i in payload.items)
    tax_amount = sum(float(i.unit_price) * float(i.quantity) * (float(i.tax_rate) / 100) for i in payload.items)
    total = subtotal + tax_amount - float(payload.discount_amount)

    invoice = Invoice(
        invoice_number=invoice_number,
        customer_name=payload.customer_name,
        customer_phone=payload.customer_phone,
        customer_email=payload.customer_email,
        currency=payload.currency,
        subtotal=subtotal,
        tax_amount=tax_amount,
        discount_amount=float(payload.discount_amount),
        total_amount=total,
        payment_method=payload.payment_method,
        created_by_id=current_user.id,
    )
    db.add(invoice)
    db.flush()

    for item in payload.items:
        db.add(
            InvoiceItem(
                invoice_id=invoice.id,
                product_id=item.product_id,
                quantity=float(item.quantity),
                unit_price=float(item.unit_price),
                tax_rate=float(item.tax_rate),
                tax_amount=float(item.unit_price) * float(item.quantity) * (float(item.tax_rate) / 100),
                discount=float(item.discount),
                line_total=float(item.unit_price) * float(item.quantity)
                + float(item.unit_price) * float(item.quantity) * (float(item.tax_rate) / 100)
                - float(item.discount),
            )
        )
        prod = db.query(Product).filter(Product.id == item.product_id).first()
        if prod:
            prod.stock_quantity = float(prod.stock_quantity) - float(item.quantity)

    db.commit()
    db.refresh(invoice)
    return invoice


@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(invoice_id: str, db: Session = Depends(get_db)):
    inv = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv


@router.get("/{invoice_id}/pdf")
def invoice_pdf(invoice_id: str, db: Session = Depends(get_db)):
    inv = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    path = generate_invoice_pdf(inv)
    return {"pdf_url": f"/static/invoices/{os.path.basename(path)}", "invoice_number": inv.invoice_number}