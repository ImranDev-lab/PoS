from fastapi import APIRouter
from ..schemas import CartCalculate, CartTotal

router = APIRouter()


@router.post("/calculate", response_model=CartTotal)
def calculate_cart(payload: CartCalculate):
    subtotal = sum(float(i.unit_price) * float(i.quantity) for i in payload.items)
    tax_amount = sum(float(i.unit_price) * float(i.quantity) * (payload.tax_rate / 100) for i in payload.items)
    total = subtotal + tax_amount - float(payload.discount_amount)
    return CartTotal(
        subtotal=subtotal,
        tax_amount=tax_amount,
        discount_amount=float(payload.discount_amount),
        total_amount=total,
    )