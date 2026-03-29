# GigLess Campus Marketplace

Full-stack university student freelancing marketplace built with Django, DRF, Channels, React, and PostgreSQL-ready configuration.

## Features Implemented

- Email/password authentication with JWT in HTTP-only cookies
- Role-based users: freelancer and customer
- Freelancer profile fields: bio, skills, rating
- Service management with categories and pricing
- Search and filter by keyword, category, price range, and rating
- Order workflow with statuses: pending, in_progress, completed
- Dummy payment marker for MVP flow
- Reviews only after completed orders
- Auto freelancer rating aggregation from reviews
- Chat data model + REST messaging endpoints + websocket consumer
- Responsive modern UI with core pages

## Project Structure

- `backend/` Django API + database models + websocket backend
- `frontend/` React UI with routing and API integration

## Single Environment Setup (Whole Project)

1. Copy `.env.example` to `.env` at the project root.
2. Use the single Python virtual environment at project root: `.venv/`.
3. Run backend and frontend from this same repository workspace.

## Backend Setup

1. Open terminal in the project root.
2. Activate the shared venv:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
python -m pip install -r .\backend\requirements.txt
```

4. Run migrations:

```powershell
python .\backend\manage.py migrate
```

5. Start backend server:

```powershell
python .\backend\manage.py runserver
```

Backend runs on `http://localhost:8000`.

## Frontend Setup

1. Open terminal in `frontend/`
2. Install dependencies:

```powershell
npm install
```

3. Run development server:

```powershell
npm run dev
```

Frontend runs on `http://localhost:5173`.

## Core API Routes

- Auth: `/api/auth/signup/`, `/api/auth/login/`, `/api/auth/logout/`, `/api/auth/refresh/`, `/api/auth/me/`
- Services: `/api/services/`, `/api/services/categories/`, `/api/services/{id}/`
- Orders: `/api/orders/`, `/api/orders/{id}/status/`, `/api/orders/{id}/review/`
- Reviews by freelancer: `/api/orders/freelancer/{freelancer_id}/reviews/`
- Chat: `/api/chat/conversations/`, `/api/chat/conversations/{id}/messages/`
- Websocket: `/ws/chat/{conversation_id}/`

## Notes

- Categories are seeded automatically via migration.
- Database defaults to SQLite for immediate local run; set PostgreSQL env vars in root `.env` (from `.env.example`) to switch.
- Payment is intentionally dummy/mock for MVP.
