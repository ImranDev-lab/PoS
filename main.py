import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import engine, init_db, Base
from .routers import auth, products, invoices, cart, ai, whatsapp, sync

app = FastAPI(title="Next-Gen Billing & POS System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static/invoices", exist_ok=True)
os.makedirs("static/qr", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(invoices.router, prefix="/invoices", tags=["Invoices"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])
app.include_router(ai.router, prefix="/ai", tags=["AI"])
app.include_router(whatsapp.router, prefix="/whatsapp", tags=["WhatsApp"])
app.include_router(sync.router, prefix="/sync", tags=["Sync"])


@app.get("/health")
def health():
    return {"status": "ok", "service": "pos-backend"}