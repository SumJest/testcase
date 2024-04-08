import logging

from api.schemas import ClientAction
from testcase.celery import app


@app.task
def log_client_action(fio: str, action: ClientAction):
    logging.info(f"{fio} ({action})")
