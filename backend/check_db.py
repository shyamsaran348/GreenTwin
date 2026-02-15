from app.database import engine, SessionLocal
from sqlalchemy import text
# Import ALL models to ensure they are registered
from app.models.plant import Plant
from app.models.user import User
from app.models.plant_state import PlantState
from app.models.plant_log import PlantLog
from app.models.disease_record import DiseaseRecord
from app.models.reminder import Reminder

# Import Schemas
from app.schemas.plant_schema import PlantOut
from app.config import settings
import os

def check_db():
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    if "sqlite" in settings.DATABASE_URL:
        db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        print(f"Resolved DB Path: {os.path.abspath(db_path)}")
        
    print("Checking database...")
    db = SessionLocal()
    try:
        # Check tables
        print("Tables in DB:")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            for row in result:
                print(f" - {row[0]}")
        
        # Check users
        users = db.query(User).all()
        print(f"Users found: {len(users)}")
        for u in users:
            print(f" - User: {u.email} (ID: {u.id})")
            
        # Check plants
        if users:
            user = users[0]
            print(f"Querying plants for user {user.id}...")
            plants = db.query(Plant).filter(Plant.user_id == user.id).all()
            print(f"Plants found: {len(plants)}")
            
            for p in plants:
                print(f"Found plant: {p.name} (ID: {p.id})")
                # Try Pydantic validation
                print("Validating against PlantOut schema...")
                try:
                    p_out = PlantOut.model_validate(p)
                    print(f"Validation successful: {p_out}")
                except Exception as e:
                    print(f"Validation failed for plant {p.id}: {e}")
                    # Print more details about the plant object
                    print(f"Plant details: {p.__dict__}")
        else:
            print("No users found to query plants for.")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_db()
