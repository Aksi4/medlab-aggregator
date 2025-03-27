from sqlalchemy.orm import Session
from database.models import LabService, GeneralService, Category, UnmatchedService

def process_lab_services(db: Session):

    lab_services = db.query(LabService).all()


    for service in lab_services:
        service_name = service.original_name
        category_name = service.category_lab

        # Перевірка винятків
        if "Пакет" in service_name:
            category = db.query(Category).filter_by(name="Пакетні дослідження").first()

            if not category:
                category = Category(name="Пакетні дослідження")
                db.add(category)
                db.commit()


            unmatched_entry = UnmatchedService(lab_service_id=service.id, category_id=category.id)
            db.add(unmatched_entry)
            db.commit()
            continue

        category = db.query(Category).filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.add(category)
            db.commit()

        general_service = db.query(GeneralService).filter_by(name=service_name).first()

        if not general_service:

            general_service = GeneralService(name=service_name, category_ids=[category.id])
            db.add(general_service)
            db.commit()
        else:

            if category.id not in general_service.category_ids:
                general_service.category_ids.append(category.id)
                db.commit()

        service.general_service_id = general_service.id
        db.commit()