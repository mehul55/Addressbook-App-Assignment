# Address Book API

A simple FastAPI-based address book app with SQLite and coordinate-based search.

## How to Run

```bash
# 1. Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the app
uvicorn main:app --reload
```

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive Swagger UI.

## Features
- Add, update, delete, and view addresses
- Store coordinates in SQLite
- Search for nearby addresses using latitude, longitude, and radius