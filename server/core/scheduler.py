from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()
    return scheduler