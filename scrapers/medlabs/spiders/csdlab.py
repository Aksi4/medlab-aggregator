# import scrapy
# import json
# import re
#
#
# class CsdLabSpider(scrapy.Spider):
#     name = 'csdlab'
#     allowed_domains = ['csdlab.ua']
#
#     start_urls = ['https://www.csdlab.ua/analyzes/page-1']
#
#     custom_settings = {
#         'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0',
#         'DOWNLOAD_DELAY': 1,
#     }
#
#     def parse(self, response):
#
#         services = response.css('tr[data-ecommerce]')
#
#         for service in services:
#             name = service.css('td.views-field-title a::text').get()
#             price = service.css('td.views-field-field-analyzes-price-site::text').get()
#             execution_time = service.css('td.views-field-field-analyzes-term-main::text').get()
#             url = f"https://www.csdlab.ua{service.css('td.views-field-title a::attr(href)').get()}"
#             data_ecommerce = service.css('tr::attr(data-ecommerce)').get()
#
#
#             try:
#                 ecommerce_data = json.loads(data_ecommerce)
#                 category = ecommerce_data.get('item_category2', 'Невідомо')
#             except json.JSONDecodeError:
#                 category = 'Невідомо'
#
#             lab_name = 'CSDLAB'
#
#
#             name = name.strip() if name else 'Невідомо'
#             price = price.strip() if price else 'Невідомо'
#             execution_time = execution_time.strip() if execution_time else 'Невідомо'
#
#
#             price = re.sub(r'\D', '', price) if price != 'Невідомо' else price
#
#             yield {
#                 'name': name,
#                 'price': price,
#                 'execution_time': execution_time,
#                 'url': url,
#                 'category': category,
#                 'lab_name': lab_name,
#             }
#
#
#         current_page = int(response.url.split('-')[-1])
#
#         if current_page < 60:
#             next_page = f'https://www.csdlab.ua/analyzes/page-{current_page + 1}'
#             yield scrapy.Request(next_page, callback=self.parse)
#         else:
#             self.log('stop')

import scrapy
import json
import re
from sqlalchemy.orm import Session
from database.models import Lab, LabService
from database import get_db


class CsdLabSpider(scrapy.Spider):
    name = 'csdlab'
    allowed_domains = ['csdlab.ua']
    start_urls = ['https://www.csdlab.ua/analyzes/page-1']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0',
        'DOWNLOAD_DELAY': 1,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records_count = 0

    def parse(self, response):

        services = response.css('tr[data-ecommerce]')

        for service in services:
            name = service.css('td.views-field-title a::text').get()
            price = service.css('td.views-field-field-analyzes-price-site::text').get()
            execution_time = service.css('td.views-field-field-analyzes-term-main::text').get()
            url = f"https://www.csdlab.ua{service.css('td.views-field-title a::attr(href)').get()}"
            data_ecommerce = service.css('tr::attr(data-ecommerce)').get()


            try:
                ecommerce_data = json.loads(data_ecommerce)
                category = ecommerce_data.get('item_category2', 'Невідомо')
            except json.JSONDecodeError:
                category = 'Невідомо'

            lab_name = 'CSDLAB'


            name = name.strip() if name else 'Невідомо'

            execution_time = execution_time.strip() if execution_time else 'Невідомо'
            price = price.strip() if price else None

            if price:
                price = re.sub(r'\D', '', price)

            self.save_to_db(name, price, execution_time, url, category, lab_name)

        current_page = int(response.url.split('-')[-1])

        if current_page < 60:
            next_page = f'https://www.csdlab.ua/analyzes/page-{current_page + 1}'
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            self.log('stop')
            self.log(f"Кількість записів: {self.records_count}")

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

        # лічильник
        self.records_count += 1

        return lab_service