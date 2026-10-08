import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from reminder import check_special_days

# Initialize the scheduler
scheduler = BlockingScheduler()

# Schedule check_special_days() to run every day at 8:00 AM
scheduler.add_job(
    check_special_days,
    trigger='cron',
    hour=8,
    minute=0
)

print("⏰ Background scheduler started successfully!")
print(f"Current System Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("🗓️ Scheduled job: Runs daily at 8:00 AM.")
print("Keep this terminal window open. Press Ctrl+C to stop.\n")

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    print("\n🛑 Scheduler stopped.")
    