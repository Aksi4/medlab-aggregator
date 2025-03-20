from sqlalchemy.orm import Session
from fuzzywuzzy import process
from collections import defaultdict

from database.models import Category, GeneralService, LabService, UnmatchedService

def process_lab_services(session: Session):

    lab_services = session.query(LabService).all()

    # список для невідповідних послуг
    unmatched_list = []


    for lab_service in lab_services:
        # Перевірка винятків
        if "Пакет" in lab_service.original_name or "Комплекс" in lab_service.original_name:


            category = session.query(Category).filter_by(name="Пакети досліджень").first()
            if not category:
                category = Category(name="Пакети досліджень")
                session.add(category)
                session.commit()

            unmatched_service = UnmatchedService(lab_service_id=lab_service.id, category_id=category.id)
            session.add(unmatched_service)

            session.commit()
            continue

        # повний збіг із general_services
        general_service = session.query(GeneralService).filter_by(name=lab_service.original_name).first()
        if general_service:
            lab_service.general_service_id = general_service.id
            session.commit()
            continue

        # частковий збіг (Fuzzy Matching)
        best_match = process.extractOne(lab_service.original_name, [gs.name for gs in session.query(GeneralService).all()])
        if best_match[1] > 85:  # якщо схожість більше 85%
            matched_general_service = session.query(GeneralService).filter_by(name=best_match[0]).first()
            lab_service.general_service_id = matched_general_service.id
            session.commit()
            continue

        # порівняння (Not finished)
        tokens = lab_service.original_name.split()
        best_match_score = 0
        best_match_name = None
        for general_service in session.query(GeneralService).all():
            general_service_tokens = general_service.name.split()
            common_tokens = set(tokens).intersection(general_service_tokens)
            score = len(common_tokens) / len(set(tokens).union(general_service_tokens)) * 100
            if score > best_match_score:
                best_match_score = score
                best_match_name = general_service.name

        if best_match_score > 80:  # 80%
            matched_general_service = session.query(GeneralService).filter_by(name=best_match_name).first()
            lab_service.general_service_id = matched_general_service.id
            session.commit()
            continue

        # винятки
        category = session.query(Category).filter_by(name="Інші дослідження").first()
        if not category:

            category = Category(name="Інші дослідження")
            session.add(category)
            session.commit()

        unmatched_service = UnmatchedService(lab_service_id=lab_service.id, category_id=category.id)
        session.add(unmatched_service)
        unmatched_list.append(lab_service)

    # Групування схожих послуг (Not finished)
    if unmatched_list:
        grouped_services = defaultdict(list)
        for service in unmatched_list:
            best_match = process.extractOne(service.original_name, [s.original_name for s in unmatched_list if s != service])
            if best_match[1] > 85:  # 85%
                grouped_services[best_match[0]].append(service)

        for group_name, group_services in grouped_services.items():
            new_general_service = GeneralService(name=group_name)
            session.add(new_general_service)
            session.commit()

            category_ids = set()
            for service in group_services:
                category = session.query(Category).filter_by(name=service.category_lab).first()
                if category:
                    category_ids.add(category.id)

            new_general_service.category_ids = list(category_ids)
            session.commit()

            for service in group_services:
                service.general_service_id = new_general_service.id
                session.commit()

    # Перевірка категорій для нових унікальних послуг
    for lab_service in lab_services:
        if lab_service.general_service_id:
            general_service = session.query(GeneralService).filter_by(id=lab_service.general_service_id).first()
            if general_service:
                category = session.query(Category).filter_by(name=lab_service.category_lab).first()
                if category and category.id not in general_service.category_ids:
                    general_service.category_ids.append(category.id)
                    session.commit()
