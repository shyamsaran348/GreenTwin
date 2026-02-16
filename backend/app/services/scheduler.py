from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models.user import User
from app.models.plant import Plant
from app.models.reminder import Reminder
from app.services.weather_service import weather_service

scheduler = BackgroundScheduler()

def check_heat_emergencies():
    """
    Background job to check for extreme heat and alert users.
    """
    print(f"[{datetime.now()}] 🌡️ Checking Heat Emergencies...")
    db = SessionLocal()
    try:
        users = db.query(User).filter(User.latitude != None).all()
        for user in users:
            # 1. Get Weather for User
            weather = weather_service.get_current_weather(user.latitude, user.longitude)
            if not weather: 
                continue
                
            temp = weather.get("temperature", 0)
            
            # 2. Check Threshold
            if temp > 35.0:
                print(f"🔥 EXTREME HEAT ({temp}°C) for User {user.email}")
                
                # 3. Create Urgent Reminders for ALL plants if not already exists today
                plants = db.query(Plant).filter(Plant.user_id == user.id).all()
                for plant in plants:
                    # Check if we already alerted today to avoid spam
                    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
                    existing = db.query(Reminder).filter(
                        Reminder.plant_id == plant.id,
                        Reminder.reminder_type == "water", # Reuse type or new 'urgent'
                        Reminder.due_date >= today_start,
                        Reminder.is_completed == False
                    ).first()
                    
                    if not existing:
                        # Create Urgent Task
                        new_reminder = Reminder(
                            plant_id=plant.id,
                            reminder_type="water",
                            message=f"🔥 HEAT EMERGENCY! {temp}°C. Water immediately!",
                            due_date=datetime.utcnow(),
                            is_completed=False
                        )
                        db.add(new_reminder)
                        print(f"   -> Created Urgent Reminder for {plant.name}")
        db.commit()
    except Exception as e:
        print(f"Scheduler Error: {e}")
    finally:
        db.close()

def smart_skip_logic():
    """
    Check if it's raining and auto-complete/skip reminders.
    """
    print(f"[{datetime.now()}] 🌧️ Checking Rain Skips...")
    db = SessionLocal()
    try:
        users = db.query(User).filter(User.latitude != None).all()
        for user in users:
            weather = weather_service.get_current_weather(user.latitude, user.longitude)
            if not weather: continue
            
            condition = weather.get("condition", "").lower()
            is_raining = "rain" in condition or "drizzle" in condition or "shower" in condition
            
            if is_raining:
                print(f"🌧️ RAIN DETECTED for User {user.email}. Skipping tasks...")
                plants = db.query(Plant).filter(Plant.user_id == user.id).all()
                for plant in plants:
                    # Find pending water reminders
                    reminders = db.query(Reminder).filter(
                        Reminder.plant_id == plant.id,
                        Reminder.reminder_type == "water",
                        Reminder.is_completed == False,
                        Reminder.due_date <= datetime.utcnow() + timedelta(hours=12)
                    ).all()
                    
                    for rem in reminders:
                        rem.is_completed = True
                        # Append a note? We don't have a notes field on reminder. 
                        # Only on PlantLog? 
                        # Ideally, we'd have a 'status' field. 
                        print(f"   -> Skipped Water Task for {plant.name}")
        db.commit()
    except Exception as e:
        print(f"Scheduler Error: {e}")
    finally:
        db.close()

def start_scheduler():
    # Check heat every 30 mins
    scheduler.add_job(check_heat_emergencies, 'interval', minutes=30)
    # Check rain skip every 60 mins
    scheduler.add_job(smart_skip_logic, 'interval', minutes=60)
    
    scheduler.start()
