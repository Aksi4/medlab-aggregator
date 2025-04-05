FROM python:3.11


WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./etl_tasks .
COPY ./database .
COPY ./scrapers .
COPY manage.py .
COPY ./app .
COPY run.py .

ENV CELERY_BROKER_URL=redis://redis:6379/0
ENV CELERY_RESULT_BACKEND=redis://redis:6379/0

EXPOSE 8000

CMD ["celery", "-A", "etl_tasks.celery", "worker", "--loglevel=info"]