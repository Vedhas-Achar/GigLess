# GigLess Campus Marketplace

Full-stack student freelancing marketplace with Django REST API + Channels websocket chat and a React (Vite) frontend.

## Current Status

Implemented and working in this repository:

- JWT auth with HTTP-only cookies (`access_token`, `refresh_token`)
- Role-based accounts (`freelancer`, `customer`)
- Profile fields and profile photo upload
- Service listing/creation with category, delivery time, pricing, optional image
- Search/filter/sort for services
- Order lifecycle (`pending -> in_progress -> completed`) with participant-only access
- Review system (only customer, only completed order, one review per order)
- Freelancer rating auto-aggregation from reviews
- REST chat + realtime websocket chat for conversation participants
- Protected frontend routes for authenticated pages

## Tech Stack

- Backend: Django 5, Django REST Framework, SimpleJWT, Channels, Daphne
- Database: SQLite by default, MySQL when DB env vars are provided
- Frontend: React 19, Vite 8, React Router, Axios

## Repository Structure

- `backend/`: Django project (`accounts`, `marketplace_services`, `orders`, `chat`, `config`)
- `frontend/`: React app
- `.env.example`: shared env template for backend + frontend

## Environment

1. Copy `.env.example` to `.env` in project root.
2. Use one Python venv at repository root (`.venv`).

Example (PowerShell):

```powershell
Copy-Item .env.example .env
```

## Backend Setup (Windows PowerShell)

```powershell
# from project root
.\.venv\Scripts\Activate.ps1
python -m pip install -r .\backend\requirements.txt
python .\backend\manage.py migrate
python .\backend\manage.py runserver
```

Backend base URL: `http://localhost:8000`

## Frontend Setup (Windows PowerShell)

```powershell
# from project root
cd .\frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

Important: `npm run dev` must be executed inside `frontend/` (or use `npm --prefix frontend run dev` from root).

## API Summary

Base prefix: `/api`

### Auth (`/api/auth/`)

- `POST /signup/`
- `POST /login/`
- `POST /logout/`
- `POST /refresh/`
- `GET/PATCH /me/`
- `GET /freelancers/{id}/`

### Services (`/api/services/`)

- `GET/POST /`
- `GET /categories/`
- `GET/PATCH/DELETE /{id}/`

Query params supported on `GET /api/services/`:

- `keyword`
- `category` (id or exact category name)
- `price_min`
- `price_max`
- `rating_min`
- `ordering` (`price`, `created_at`, `-price`, `-created_at`)

### Orders (`/api/orders/`)

- `GET/POST /`
- `GET /{id}/`
- `PATCH /{id}/status/`
- `POST /{order_id}/review/`
- `GET /freelancer/{freelancer_id}/reviews/`

Status rules:

- Only freelancer can set `in_progress`
- Only customer can set `completed`

### Chat (`/api/chat/` + websocket)

- `GET/POST /conversations/`
- `GET/POST /conversations/{conversation_id}/messages/`
- `GET /ws-token/` (returns JWT token for websocket query param)

WebSocket endpoint:

- `/ws/chat/{conversation_id}/?token=<jwt>`

## Media Uploads

- Profile photos: `backend/media/profiles/`
- Service images: `backend/media/services/`

## Database Configuration

Current backend settings use:

- SQLite when `DB_NAME` is not set
- MySQL when `DB_NAME` is set (with `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`)

If switching to MySQL, make sure those `DB_*` variables exist in `.env`.

## Notes

- Categories are seeded via migrations.
- Payment is intentionally mock (`dummy_payment_status`) for MVP flow.
- Channels layer is currently in-memory, suitable for local development.
