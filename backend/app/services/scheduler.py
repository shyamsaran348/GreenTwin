from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
# In a real app, this would query DB and send notifications
# For now, it just prints a message

scheduler = BackgroundScheduler()

def check_reminders():
    print(f"[{datetime.now()}] Checking for due reminders...")
    # Logic to fetch due reminders from DB and alert user
    # This requires creating a new DB session inside this job
    pass

def start_scheduler():
    scheduler.add_job(check_reminders, 'interval', minutes=60)
    scheduler.start()
