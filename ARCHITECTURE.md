# System Architecture — Next-Gen Billing & POS

## Overview
A modular, offline-first Billing & Point-of-Sale system for small-to-medium retail and service businesses (Pakistan-first, multi-currency, FBR-tax ready).

## High-Level Architecture
```
┌─────────────────┐      HTTPS/WSS      ┌──────────────────────┐
│  React + Tailwind│◄──────────────────►│  FastAPI (Python)    │
│  (Web/PWA/Desktop)│                    │  (REST + JWT Auth)   │
└─────────────────┘                    └──────────┬───────────┘
                                                   │
                                    ┌──────────────▼──────────────┐
                                    │  Cloud: PostgreSQL (Supabase)│
                                    │  Local: SQLite (offline)    │
                                    └──────────────┬──────────────┘
                                                   │
          ┌──────────────┬──────────────┬─────────┼─────────┐
          ▼              ▼              ▼         ▼         ▼
     PDF Invoices   QR Payments   WhatsApp   AI Stock   AI Voice/OCR
     (ReportLab)    (qrcode)      (Twilio)   Prediction (Whisper/OpenAI)
```

## Key Design Decisions
- **Backend:** FastAPI + SQLAlchemy 2.0 + Pydantic v2. Async-ready, modular routers/services.
- **Database:** Single SQLAlchemy model layer works against SQLite (local/PWA) or PostgreSQL (cloud). Switch via `DATABASE_URL`.
- **Offline-First:** `offline_sync_queue` outbox table. Client queues inserts/updates/deletes; `/sync/bulk` applies them when connectivity returns.
- **Multi-tenancy:** Not implemented in v1; add `tenant_id` to all tables for SaaS multi-tenant isolation.
- **AI:** OpenAI Whisper for voice transcription, OpenAI Vision / PyTesseract for OCR, simple moving-average stock prediction (upgradeable to Prophet/ARIMA).
- **Payments:** Dynamic JazzCash/EasyPaisa-compatible QR payloads generated per invoice.
- **Delivery:** WhatsApp Cloud API / Twilio placeholder service; swap credentials in `.env`.

## Module Map
| Module | Responsibility |
|--------|----------------|
| `app/models.py` | SQLAlchemy ORM models |
| `app/schemas.py` | Pydantic request/response schemas |
| `app/deps.py` | DB session + JWT auth dependency |
| `app/routers/auth.py` | Login / JWT |
| `app/routers/products.py` | CRUD + low-stock |
| `app/routers/invoices.py` | Invoice CRUD + PDF generation |
| `app/routers/cart.py` | Cart total calculation |
| `app/routers/ai.py` | Voice-to-bill, OCR, stock prediction |
| `app/routers/whatsapp.py` | WhatsApp invoice delivery |
| `app/routers/sync.py` | Offline sync queue |
| `app/services/*` | Business logic (PDF, QR, AI, WhatsApp, Sync) |

## Security Notes
- Change `SECRET_KEY` in production.
- Use HTTPS + strong CORS origins.
- Hash passwords with bcrypt (passlib).
- Validate all inputs via Pydantic; never trust client totals.