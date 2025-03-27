
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from config import DATABASE_URL
from subprocess import run
from database.initial_services import process_lab_services as initial_process
from database.map_services import process_lab_services as map_process

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def reset_db():
    Base.metadata.drop_all(engine)
    print("database reset!")

def create_db():
    reset_db()
    Base.metadata.create_all(engine)
    print("database created!")


def run_scrapy_crawl(spider_name):
    print(f"starting scrapy crawl for {spider_name}...")
    try:
        # відносний шлях
        result = run(['scrapy', 'crawl', spider_name], cwd='scrapers')
        if result.returncode != 0:
            print(f"Error running {spider_name}")
        else:
            print(f"{spider_name} completed successfully!")
    except Exception as e:
        print(f"Error occurred while running {spider_name}: {e}")

def main():

    reset_db()
    create_db()


    run_scrapy_crawl('diameb')


    db = SessionLocal()
    try:
        initial_process(db)
    finally:
        db.close()

    run_scrapy_crawl('csdlab')
    run_scrapy_crawl('synevo')
    run_scrapy_crawl('primamed')


    db = SessionLocal()
    try:
        map_process(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
