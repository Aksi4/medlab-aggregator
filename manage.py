import sys
from etl_tasks.celery import celery
from subprocess import run

def start_celery_worker():
    run(['celery', '-A', 'etl_tasks.celery', 'worker', '--loglevel=info'])

def start_celery_beat():
    run(['celery', '-A', 'etl_tasks.celery', 'beat', '--loglevel=info', '--scheduler=redbeat.RedBeatScheduler'])

def run_etl_task():
    print("Running ETL task...")
    celery.send_task('etl_tasks.celery.run_etl')

def main():
    if len(sys.argv) < 2:
        print("Usage: manage.py [celery-worker|celery-beat|run-etl]")
        sys.exit(1)

    command = sys.argv[1]
    if command == 'celery-worker':
        start_celery_worker()
    elif command == 'celery-beat':
        start_celery_beat()
    elif command == 'run-etl':
        run_etl_task()
    else:
        print(f"Unknown command {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()