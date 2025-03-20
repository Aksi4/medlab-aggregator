
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)


def reset_db():
    Base.metadata.drop_all(engine)
    print("database reset!")


def create_db():
    reset_db()
    Base.metadata.create_all(engine)
    print("database created!")

#при подальшій розробці відключити елемент скидання та створення і підключити оновлення бази


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == '__main__':
    create_db()
