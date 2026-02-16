from sqlalchemy import create_engine, text
from app.config import settings

def migrate():
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE plants ADD COLUMN image_path VARCHAR"))
            conn.commit()
            print("Migration successful: Added image_path to plants table.")
        except Exception as e:
            print(f"Migration failed (might already exist): {e}")

if __name__ == "__main__":
    migrate()
