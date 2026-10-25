from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models import Product, AIStockPrediction


def predict_stock(db: Session, product_id: str):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    stock = float(product.stock_quantity)
    if stock <= 0:
        days = 0
        rec = float(product.reorder_level)
    else:
        avg_daily = max(float(product.reorder_level) - stock, 1.0)
        days = int(stock / avg_daily)
        rec = float(product.reorder_level)

    return AIStockPrediction(
        product_id=product.id,
        predicted_stock_out_date=datetime.utcnow() + timedelta(days=days),
        days_until_stockout=days,
        recommended_reorder_quantity=rec,
        confidence_score=0.75,
    )