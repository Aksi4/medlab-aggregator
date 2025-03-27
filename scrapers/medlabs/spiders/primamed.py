
import scrapy
from sqlalchemy.orm import Session
from database.models import Lab, LabService
from database import get_db


class PrimamedSpider(scrapy.Spider):
    name = 'primamed'
    start_urls = ['https://primamed.if.ua/dostupni-analizy/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records_count = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        current_category = None
        rows = response.xpath('//table[@class="table-striped table table-bordered"]/tbody/tr')

        previous_service = None

        for index, row in enumerate(rows):
            category_element = row.xpath('.//td[contains(@class, "table-primary")]/span/text()').get()

            if category_element:
                current_category = category_element.strip()
            else:
                hidden_url = row.xpath('.//a[contains(@class, "btn-primary")]/@href').get()

                if 'display:none' in row.get():
                    if previous_service and hidden_url:
                        previous_service['url'] = hidden_url
                    yield previous_service
                    previous_service = None
                    continue

                if previous_service:
                    yield previous_service

                service_name = row.xpath('.//td/p[contains(@class, "title")]/text()').get()

                if service_name:
                    service_name = service_name.strip()
                    price = row.xpath('.//td/p[contains(@class, "snippet")]/text()').get()
                    price = price.strip() if price else "не вказано"
                    service_url = row.xpath('.//a[contains(@class, "btn-primary")]/@href').get()
                    service_url = service_url if service_url else 'https://primamed.if.ua/dostupni-analizy/'

                    execution_time = None


                    self.save_to_db(
                        service_name=service_name,
                        price=price,
                        execution_time=execution_time,
                        url=service_url,
                        category=current_category,
                        lab_name="Прімамед")


        if previous_service:
            yield previous_service

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

        self.records_count += 1  # лічильник

        return lab_service

    def close(self, reason):

        print(f"Кількість записів: {self.records_count}")
