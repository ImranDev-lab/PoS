# Backend API Endpoints

Base URL: `http://localhost:8000`

## Auth
| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| POST | `/auth/login` | `{username, password}` | JWT login |
| GET | `/auth/me` | Bearer token | Current user |

## Products
| Method | Endpoint | Query/Body | Description |
|--------|----------|------------|-------------|
| GET | `/products/` | `?search=&skip=&limit=` | List products |
| POST | `/products/` | ProductCreate | Create product |
| GET | `/products/{id}` | - | Get product |
| PATCH | `/products/{id}` | ProductUpdate | Update product |
| GET | `/products/low-stock` | - | Low stock items |

## Invoices
| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| POST | `/invoices/` | InvoiceCreate | Create invoice from cart |
| GET | `/invoices/{id}` | - | Get invoice |
| GET | `/invoices/{id}/pdf` | - | Returns `{pdf_url, invoice_number}` |

## Cart
| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| POST | `/cart/calculate` | CartCalculate | Compute subtotal/tax/total |

## AI
| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| POST | `/ai/voice-to-bill` | multipart audio | Whisper transcription + item parse |
| POST | `/ai/ocr-invoice` | multipart image/pdf | Supplier invoice OCR |
| POST | `/ai/stock-prediction/{id}` | - | Generate stock-out prediction |
| GET | `/ai/stock-predictions` | - | List predictions |

## WhatsApp
| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| POST | `/whatsapp/send-invoice` | `{invoice_id, phone, message?}` | Send invoice to WhatsApp |

## Sync (Offline-First)
| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| GET | `/sync/pending` | - | Pending sync queue |
| POST | `/sync/bulk` | `[{table_name, record_id, operation, payload}]` | Apply offline changes |

## Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Service health |

## Notes
- All mutating endpoints require `Authorization: Bearer <jwt>` except `/auth/login`.
- Static files served at `/static/invoices/*.pdf` and `/static/qr/*.png`.
- Replace `DATABASE_URL` with PostgreSQL for cloud/Supabase deployment.