from sqlalchemy import create_engine, text
from app.database import SQLALCHEMY_DATABASE_URL

def migrate():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    with engine.connect() as conn:
        try:
            # Check if column exists (simple try/except for SQLite/PG generic approach)
            # SQLite doesn't support IF NOT EXISTS in ADD COLUMN easily, but we can try
            print("Migrating Users table...")
            conn.execute(text("ALTER TABLE users ADD COLUMN latitude FLOAT"))
            conn.execute(text("ALTER TABLE users ADD COLUMN longitude FLOAT"))
            print("Added lat/lon to users.")
        except Exception as e:
            print(f"Migration note (might already exist): {e}")

if __name__ == "__main__":
    migrate()
