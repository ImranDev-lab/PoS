import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from ..models import Invoice


def generate_invoice_pdf(invoice: Invoice) -> str:
    os.makedirs("static/invoices", exist_ok=True)
    filename = f"invoice_{invoice.invoice_number}.pdf"
    path = os.path.join("static/invoices", filename)

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "TAX INVOICE")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"Invoice #: {invoice.invoice_number}")
    c.drawString(50, height - 85, f"Date: {invoice.created_at.strftime('%Y-%m-%d %H:%M')}")
    c.drawString(50, height - 100, f"Customer: {invoice.customer_name or 'Walk-in'}")
    c.drawString(50, height - 115, f"Phone: {invoice.customer_phone or '-'}")

    y = height - 150
    c.drawString(50, y, "Item")
    c.drawString(200, y, "Qty")
    c.drawString(250, y, "Price")
    c.drawString(320, y, "Total")
    y -= 20

    for item in invoice.items:
        name = item.product.name if item.product else "Product"
        c.drawString(50, y, name[:40])
        c.drawString(200, y, str(item.quantity))
        c.drawString(250, y, f"{item.unit_price:.2f}")
        c.drawString(320, y, f"{item.line_total:.2f}")
        y -= 20

    c.drawString(50, y - 20, f"Subtotal: {invoice.subtotal:.2f}")
    c.drawString(50, y - 35, f"Tax: {invoice.tax_amount:.2f}")
    c.drawString(50, y - 50, f"Discount: {invoice.discount_amount:.2f}")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y - 70, f"Total: {invoice.total_amount:.2f} {invoice.currency}")
    c.save()
    return path