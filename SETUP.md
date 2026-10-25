# Setup Instructions

## Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend)
- PostgreSQL (optional; SQLite used by default)

## 1. Backend (FastAPI)

```bash
cd pos-system/backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edit .env if using PostgreSQL or OpenAI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend API: `http://localhost:8000`  
Docs: `http://localhost:8000/docs`

### Docker (backend + Postgres)
```bash
cd pos-system/backend
docker-compose up --build
```

## 2. Frontend (React + Vite + Tailwind)

```bash
cd pos-system/frontend
npm install
npm run dev        # http://localhost:5173
npm run build      # production build
```

The Vite dev server proxies `/api` to `http://localhost:8000`.

## 3. Default Seed (Optional)
Create an admin/cashier user via the `/auth/login` endpoint after inserting a user row, or add a seed script to `app/database.py`:

```python
from passlib.context import CryptContext
pwd = CryptContext(schemes=["bcrypt"])
# insert user with username='admin', password_hash=pwd.hash('admin123')
```

## 4. Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./pos_local.db` | SQLite for local, PostgreSQL for cloud |
| `SECRET_KEY` | `dev-secret-change-me` | JWT signing key |
| `OPENAI_API_KEY` | - | Whisper + Voice parsing |
| `TWILIO_*` | - | WhatsApp delivery (optional) |

## 5. Production Checklist
- Set strong `SECRET_KEY`.
- Restrict CORS origins.
- Run Alembic migrations against PostgreSQL.
- Serve static files via Nginx/CDN.
- Configure Twilio/Meta WhatsApp credentials.
- Enable HTTPS.