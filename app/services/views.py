from flask import render_template, request, flash
from sqlalchemy.orm import joinedload
from sqlalchemy import asc, desc
from . import sort_bp
from database import get_db
from database.models import Category, GeneralService, LabService, Lab, UnmatchedService

@sort_bp.route('/general_services', methods=['GET'])
def general_services():
    db = next(get_db())

    categories = db.query(Category).all()
    selected_category_id = request.args.get('category', type=int)
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    search = request.args.get('search', type=str)
    sort_by = request.args.get('sort_by', default='name', type=str)
    sort_order = request.args.get('sort_order', default='asc', type=str)

    order = asc if sort_order == 'asc' else desc

    # еталонні послуги
    query = db.query(GeneralService).options(joinedload(GeneralService.lab_services).joinedload(LabService.lab))

    if selected_category_id:
        query = query.filter(GeneralService.category_ids.any(selected_category_id))

    if search:
        query = query.filter(GeneralService.name.ilike(f'%{search}%'))

    services = query.all()
    has_general_services = bool(services)

    if has_general_services:
        filtered_services = []
        checked_lab_services = []
        for service in services:
            unique_lab_services = []
            for lab_service in service.lab_services:
                if (min_price is None or lab_service.price >= min_price) and (
                        max_price is None or lab_service.price <= max_price):
                    is_duplicate = any(
                        existing_service['name'] == lab_service.original_name and
                        existing_service['lab_name'] == lab_service.lab.lab_name
                        for existing_service in checked_lab_services
                    )
                    if not is_duplicate:
                        unique_lab_services.append(lab_service)
                        checked_lab_services.append(
                            {'name': lab_service.original_name, 'lab_name': lab_service.lab.lab_name})

            if unique_lab_services:
                service.lab_services = unique_lab_services
                # перевірка, щоб не додавати еталонну послугу, яка має лише одну лабораторну послугу
                if len(service.lab_services) > 1:
                    filtered_services.append(service)


        if sort_by == 'price':
            filtered_services.sort(
                key=lambda s: min((ls.price for ls in s.lab_services), default=float('inf')),
                reverse=(sort_order == 'desc')
            )
        elif sort_by == 'name':
            filtered_services.sort(
                key=lambda s: min((ls.original_name for ls in s.lab_services), default=""),
                reverse=(sort_order == 'desc')
            )

        return render_template(
            'general_services.html',
            services=filtered_services,
            categories=categories,
            selected_category_id=selected_category_id,
            min_price=min_price,
            max_price=max_price,
            sort_by=sort_by,
            sort_order=sort_order,
            search=search,
            has_general_services=True
        )

    else:
        # послуги лабораторій без еталонних
        unmatched_services = db.query(UnmatchedService).filter(
            UnmatchedService.category_id == selected_category_id).all()
        lab_service_ids = [unmatched_service.lab_service_id for unmatched_service in unmatched_services]
        lab_services_query = db.query(LabService).filter(LabService.id.in_(lab_service_ids))


        if search:
            lab_services_query = lab_services_query.filter(LabService.original_name.ilike(f'%{search}%'))


        if min_price is not None:
            lab_services_query = lab_services_query.filter(LabService.price >= min_price)
        if max_price is not None:
            lab_services_query = lab_services_query.filter(LabService.price <= max_price)

        lab_services = lab_services_query.all()


        if sort_by == 'name':
            lab_services.sort(
                key=lambda ls: ls.original_name.lower() if ls.original_name else '',
                reverse=(sort_order == 'desc')
            )
        elif sort_by == 'price':
            lab_services.sort(
                key=lambda ls: ls.price if ls.price is not None else float('inf'),
                reverse=(sort_order == 'desc')
            )

        return render_template(
            'general_services.html',
            services=lab_services,
            categories=categories,
            selected_category_id=selected_category_id,
            min_price=min_price,
            max_price=max_price,
            sort_by=sort_by,
            sort_order=sort_order,
            search=search,
            has_general_services=False
        )



@sort_bp.route('/all_services', methods=['GET'])
def all_services():
    db = next(get_db())

    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    search = request.args.get('search', type=str)
    sort_by = request.args.get('sort_by', default='name', type=str)
    sort_order = request.args.get('sort_order', default='asc', type=str)
    selected_lab = request.args.get('selected_lab', type=int)

    order = asc if sort_order == 'asc' else desc


    labs = db.query(Lab).all()


    query = db.query(LabService).join(Lab).options(joinedload(LabService.lab))

    if search:
        query = query.filter(LabService.original_name.ilike(f'%{search}%'))

    if min_price is not None:
        query = query.filter(LabService.price >= min_price)
    if max_price is not None:
        query = query.filter(LabService.price <= max_price)


    if selected_lab:
        query = query.filter(LabService.lab_id == selected_lab)

    lab_services = query.all()

    lab_services = [service for service in lab_services if service.price and service.price > 10]


    if sort_by == 'price':
        lab_services.sort(key=lambda ls: ls.price if ls.price is not None else float('inf'),
                          reverse=(sort_order == 'desc'))
    elif sort_by == 'name':
        lab_services.sort(
            key=lambda ls: ls.original_name.lower() if ls.original_name else '',
            reverse=(sort_order == 'desc')
        )
    elif sort_by == 'lab_name':
        lab_services.sort(
            key=lambda ls: ls.lab.name.lower() if ls.lab and ls.lab.name else '',
            reverse=(sort_order == 'desc')
        )

    return render_template(
        'all_services.html',
        services=lab_services,
        labs=labs,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        sort_order=sort_order,
        search=search,
        selected_lab=selected_lab
    )


