from celery import Celery
from dotenv import load_dotenv
import os,utils

load_dotenv()
celery_ap = Celery(
    "worker",
    broker=os.environ.get("CLOUDAMQP_URL"),
)
celery_ap.conf.task_routes = {
    "utils.send_email.send_email_task": {"queue": "emails"},
}
celery_ap.autodiscover_tasks(["utils.send_email"])