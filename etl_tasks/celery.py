from celery import Celery
from database.initial_services import process_lab_services as initial_process
from database.map_services import process_lab_services as map_process
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from config import DATABASE_URL
from subprocess import run


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def reset_db():
    Base.metadata.drop_all(engine)
    print("Database reset!")


def create_db():
    reset_db()
    Base.metadata.create_all(engine)
    print("Database created!")


def run_scrapy_crawl(spider_name):
    print(f"Starting scrapy crawl for {spider_name}...")
    try:
        result = run(['scrapy', 'crawl', spider_name], cwd='scrapers')
        if result.returncode != 0:
            print(f"Error running {spider_name}")
        else:
            print(f"{spider_name} completed successfully!")
    except Exception as e:
        print(f"Error occurred while running {spider_name}: {e}")

def make_celery():
    celery = Celery(
        "etl_tasks",
        broker="redis://redis:6379/0",
        backend="redis://redis:6379/0",
    )

    celery.conf.beat_scheduler = 'redbeat.RedBeatScheduler'
    celery.conf.redbeat_redis_url = 'redis://redis:6379/0'
    celery.conf.redbeat_key_prefix = 'redbeat:'

    celery.conf.timezone = 'UTC'
    celery.conf.beat_schedule = {
        "run_etl_every_month": {
            "task": "etl_tasks.celery.run_etl",
            "schedule": 2592000.0,  # 30 дн 2592000, 20 хв 1200
            "args": (),
            'options': {
                'expires': 3600,
            }
        },
    }
    celery.autodiscover_tasks(["etl_tasks"])
    return celery


celery = make_celery()

@celery.task(bind=True)
def run_etl(self):
    print("[ETL] Starting database update")
    reset_db()
    create_db()

    print("[ETL] Running Scrapy: diameb")
    run_scrapy_crawl("diameb")

    db = SessionLocal()
    try:
        print("[ETL] Primary data processing")
        initial_process(db)
    finally:
        db.close()

    for source in ["csdlab", "synevo", "primamed"]:
        print(f"[ETL] Running Scrapy: {source}")
        run_scrapy_crawl(source)

    db = SessionLocal()
    try:
        print("[ETL] Mapping services processing")
        map_process(db)
    finally:
        db.close()

    print("[ETL] Finished")