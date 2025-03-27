from sqlalchemy.orm import Session
from fuzzywuzzy import process
from collections import defaultdict

from database.models import Category, GeneralService, LabService, UnmatchedService

# стоп-сліва
STOPWORDS = {"в", "на", "аналіз", "дослідження", "натще", "та", "і", "із"}

def clean_tokens(name):
    return [word for word in name.split() if word.lower() not in STOPWORDS]

def process_lab_services(session: Session):
    lab_services = session.query(LabService).all()

    unmatched_list = []

    for lab_service in lab_services:

        if "Пакет" in lab_service.original_name or "Комплекс" in lab_service.original_name or "ChekUp" in lab_service.original_name or "Комплекс" in lab_service.original_name or "Комплекс" in lab_service.original_name:
            category = session.query(Category).filter_by(name="Пакетні дослідження").first()
            if not category:
                category = Category(name="Пакетні дослідження")
                session.add(category)
                session.commit()

            unmatched_service = UnmatchedService(lab_service_id=lab_service.id, category_id=category.id)
            session.add(unmatched_service)
            session.commit()
            continue


        general_service = session.query(GeneralService).filter_by(name=lab_service.original_name).first()
        if general_service:
            lab_service.general_service_id = general_service.id
            session.commit()
            continue



        best_match = process.extractOne(lab_service.original_name,
                                        [gs.name for gs in session.query(GeneralService).all()])

        if best_match and best_match[1] > 85 and len(best_match[0]) > len(
                lab_service.original_name) * 1.5:
            matched_general_service = session.query(GeneralService).filter_by(name=best_match[0]).first()

            if all(keyword in matched_general_service.name for keyword in lab_service.original_name.split() if
                   len(keyword) > 3):
                lab_service.general_service_id = matched_general_service.id
                session.commit()
                continue


        category = session.query(Category).filter_by(name="Інші послуги").first()
        if not category:
            category = Category(name="Інші послуги")
            session.add(category)
            session.commit()

        unmatched_service = UnmatchedService(lab_service_id=lab_service.id, category_id=category.id)
        session.add(unmatched_service)
        unmatched_list.append(lab_service)
