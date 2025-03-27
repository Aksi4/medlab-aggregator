from sqlalchemy import (
    Column, Integer, String, ForeignKey, DECIMAL, ARRAY, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

# еталонні послуги
class GeneralService(Base):
    __tablename__ = 'general_services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=True, nullable=False)
    category_ids = Column(ARRAY(Integer))  # Масив категорій

# лабораторії
class Lab(Base):
    __tablename__ = 'labs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lab_name = Column(String(255), unique=True, nullable=False)


# таблиця послуг лабораторій
class LabService(Base):
    __tablename__ = 'lab_services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lab_id = Column(Integer, ForeignKey('labs.id'), nullable=False)

    original_name = Column(Text, nullable=False)
    general_service_id = Column(Integer, ForeignKey('general_services.id'), nullable=True)
    category_lab = Column(String(255), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=True)
    execution_time = Column(String(255), nullable=True)
    url = Column(String(255), nullable=False)

    lab = relationship("Lab", backref="services")
    general_service = relationship("GeneralService", backref="lab_services")

# невідповідні послуги
class UnmatchedService(Base):
    __tablename__ = 'unmatched_services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lab_service_id = Column(Integer, ForeignKey('lab_services.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    lab_service = relationship("LabService", backref="unmatched_entries")
    category = relationship("Category", backref="unmatched_services")
