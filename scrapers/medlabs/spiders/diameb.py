
# запис в json
# import scrapy
# import json
#
#
# class ServicesSpider(scrapy.Spider):
#     name = 'diameb'
#     allowed_domains = ['diameb.com']
#     start_urls = ['https://diameb.com/api/services/categories']
#
#
#     custom_settings = {
#         'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0'
#     }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.existing_records = set()
#
#     def parse(self, response):
#
#         categories_data = json.loads(response.text)
#         self.category_map = {cat["id"]: cat["name"] for cat in categories_data}
#
#         for category in categories_data:
#             category_id = category['id']
#             category_url = f"https://diameb.com/api/services?category_id={category_id}"
#
#
#             yield scrapy.Request(url=category_url, callback=self.parse_services)
#
#     def parse_services(self, response):
#
#         services_data = json.loads(response.text)
#
#         for service in services_data:
#             if not service.get('categories'):
#                 continue
#
#             first_subcategory = service['categories'][0]
#             subcategory_id = first_subcategory["id"]
#             subcategory_name = first_subcategory["name"]
#             parent_category_id = first_subcategory["parentId"]
#
#             category_name = self.category_map.get(parent_category_id, "Невідома категорія")
#
#             url = f"https://diameb.com/services/{service['code']}?category={parent_category_id}&subCategory={subcategory_id}&service={service['id']}"
#
#             for subcategory in service['categories']:
#                 record = (
#                     service['name'],
#                     service['price'],
#                     service['term'],
#                     url,
#                     subcategory["name"],
#                     'Diameb'
#                 )
#
#                 if record not in self.existing_records:
#                     self.existing_records.add(record)
#                     yield {
#                         'name': service['name'],
#                         'price': service['price'],
#                         'execution_time': service['term'],
#                         'url': url,
#                         'category': subcategory["name"],
#                         'lab_name': 'Diameb',
#                     }
###############

import scrapy
import json
from sqlalchemy.orm import Session
from database.models import Lab, LabService
from database import get_db


class ServicesSpider(scrapy.Spider):
    name = 'diameb'
    allowed_domains = ['diameb.com']
    start_urls = ['https://diameb.com/api/services/categories']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.existing_records = set()

    def parse(self, response):
        categories_data = json.loads(response.text)
        self.category_map = {cat["id"]: cat["name"] for cat in categories_data}

        for category in categories_data:
            category_id = category['id']
            category_url = f"https://diameb.com/api/services?category_id={category_id}"

            yield scrapy.Request(url=category_url, callback=self.parse_services)

    def parse_services(self, response):
        services_data = json.loads(response.text)

        for service in services_data:
            if not service.get('categories'):
                continue

            first_subcategory = service['categories'][0]
            subcategory_id = first_subcategory["id"]
            subcategory_name = first_subcategory["name"]
            parent_category_id = first_subcategory["parentId"]

            category_name = self.category_map.get(parent_category_id, "Невідома категорія")

            url = f"https://diameb.com/services/{service['code']}?category={parent_category_id}&subCategory={subcategory_id}&service={service['id']}"

            for subcategory in service['categories']:
                record = (
                    service['name'],
                    service['price'],
                    service['term'],
                    url,
                    subcategory["name"],
                    'Diameb'
                )

                if record not in self.existing_records:
                    self.existing_records.add(record)
                    yield self.save_to_db(
                        service_name=service['name'],
                        price=service['price'],
                        execution_time=service['term'],
                        url=url,
                        category=subcategory["name"],
                        lab_name='Diameb'
                    )

    def save_to_db(self, service_name, price, execution_time, url, category, lab_name):

        db: Session = next(get_db())


        lab = db.query(Lab).filter(Lab.lab_name == lab_name).first()
        if not lab:
            lab = Lab(lab_name=lab_name)
            db.add(lab)
            db.commit()

        lab_service = LabService(
            lab_id=lab.id,
            original_name=service_name,
            category_lab=category,
            price=price,
            execution_time=execution_time,
            url=url
        )
        db.add(lab_service)
        db.commit()

        return lab_service



