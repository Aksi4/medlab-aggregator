from database import SessionLocal
from database.map_services import process_lab_services

def main():
    db = SessionLocal()
    try:
        process_lab_services(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
