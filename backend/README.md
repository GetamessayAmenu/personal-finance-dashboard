# SmartSpend Backend (FastAPI)

## Run locally with SQLite (default)
1. python -m venv venv
2. source venv/bin/activate  # or venv\Scripts\activate on Windows
3. pip install -r requirements.txt
4. uvicorn app.main:app --reload

## Notes
- By default this starter uses SQLite for convenience. Replace DATABASE_URL in .env for Postgres.
