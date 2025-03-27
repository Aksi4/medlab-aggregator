
import scrapy
import re
from sqlalchemy.orm import Session
from database.models import Lab, LabService
from database import get_db


class SynevoSpider(scrapy.Spider):
    name = 'synevo'
    allowed_domains = ['synevo.ua']
    start_urls = ['https://www.synevo.ua/rubricator']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'ROBOTSTXT_OBEY': False,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.existing_records = set()
        self.records_count = 0

    def parse(self, response):
        sections = response.xpath('//a[contains(@class, "analyze-categories__item")]/@href').getall()

        for section in sections:
            section_url = response.urljoin(section)
            yield scrapy.Request(url=section_url, callback=self.parse_subcategories)

    def parse_subcategories(self, response):
        subcategories = response.xpath('//a[contains(@href, "/rubricator/disease/")]')

        for subcategory in subcategories:
            subcategory_name = subcategory.xpath('text()').get().strip()
            subcategory_url = response.urljoin(subcategory.xpath('@href').get())

            yield scrapy.Request(url=subcategory_url, callback=self.parse_services,
                                 meta={'subcategory': subcategory_name})

    def parse_services(self, response):
        subcategory_name = response.meta['subcategory']

        services = response.xpath('//tr[contains(@class, "search__results__table__tr")]')
        for service in services:
            name = service.xpath('.//div[@class="search__results__table-name hoverable"]/a//text()').getall()
            name = " ".join(name).strip()
            name = re.sub(r'^\d+\s*', '', name)  # видаляємо цифри на початку

            price = service.xpath('.//div[@class="search__results__table-price"]/b/text()').get()
            execution_time = service.xpath('.//div[@class="search__results__table-price"]/span/text()').get()

            url = response.urljoin(
                service.xpath('.//div[@class="search__results__table-name hoverable"]/a/@href').get())
            # дн.
            if execution_time:
                execution_time = re.sub(r'(\d+)', r'\1 дн.', execution_time)

            lab_name = 'Synevo'


            record = (name, price, execution_time, url, subcategory_name, lab_name)

            if record not in self.existing_records:
                self.existing_records.add(record)
                yield self.save_to_db(
                    service_name=name,
                    price=price,
                    execution_time=execution_time,
                    url=url,
                    category=subcategory_name,
                    lab_name=lab_name
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
            execution_time=execution_time if execution_time else None,
            url=url
        )
        db.add(lab_service)
        db.commit()

        # лічильник
        self.records_count += 1

        return lab_service

    def closed(self, reason):

        print(f"Кількість записів: {self.records_count}")

