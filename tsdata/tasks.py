from celery.utils.log import get_task_logger
from nc.data.importer import run as nc_run
from md.data.importer import run as md_run
from traffic_stops.celery import app
from tsdata.models import Dataset, Import
from django.utils import timezone


logger = get_task_logger(__name__)

RUN_MAP = {
    'nc': nc_run,
    'md': md_run,
}


@app.task
def import_dataset(dataset_id):
    """Execute a state dataset import process"""
    logger.info("Received Dataset ID: {}".format(dataset_id))
    dataset = Dataset.objects.get(pk=dataset_id)
    run = Import.objects.create(dataset=dataset)
    logger.info("Starting {} import".format(dataset.state))
    state_import = RUN_MAP[run.dataset.state]
    try:
        state_import(dataset.url, destination=dataset.destination)
    except:
        run.date_finished = timezone.now()
        run.save()
        raise
    run.successful = True
    run.date_finished = timezone.now()
    run.save()
    logger.info("Import complete")
