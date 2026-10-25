from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class ProductBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    barcode: Optional[str] = None
    unit: str = "pcs"
    cost_price: Decimal = 0
    selling_price: Decimal
    tax_rate: Decimal = 0
    stock_quantity: Decimal = 0
    reorder_level: Decimal = 10
    low_stock_threshold: Decimal = 5
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    selling_price: Optional[Decimal] = None
    stock_quantity: Optional[Decimal] = None
    reorder_level: Optional[Decimal] = None
    low_stock_threshold: Optional[Decimal] = None


class ProductOut(ProductBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class InvoiceItemBase(BaseModel):
    product_id: UUID
    quantity: Decimal
    unit_price: Decimal
    tax_rate: Decimal = 0
    discount: Decimal = 0


class InvoiceItemOut(InvoiceItemBase):
    id: UUID
    line_total: Decimal

    class Config:
        from_attributes = True


class InvoiceBase(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    currency: str = "PKR"
    discount_amount: Decimal = 0
    payment_method: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    items: List[InvoiceItemBase]


class InvoiceOut(InvoiceBase):
    id: UUID
    invoice_number: str
    subtotal: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    payment_status: str
    status: str
    created_at: datetime
    items: List[InvoiceItemOut] = []

    class Config:
        from_attributes = True


class CartItem(BaseModel):
    product_id: UUID
    quantity: Decimal
    unit_price: Decimal
    tax_rate: Decimal = 0
    discount: Decimal = 0


class CartCalculate(BaseModel):
    items: List[CartItem]
    discount_amount: Decimal = 0
    tax_rate: Decimal = 0


class CartTotal(BaseModel):
    subtotal: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class AILogOut(BaseModel):
    id: UUID
    action_type: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True