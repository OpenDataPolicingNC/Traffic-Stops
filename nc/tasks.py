from datetime import timedelta
import os
import shutil

from celery.utils.log import get_task_logger
from django.conf import settings
from django.utils.timezone import now

from nc.data.importer import MAGIC_NC_FTP_URL
from traffic_stops.celery import app
from tsdata.models import Dataset
from tsdata.tasks import import_dataset

logger = get_task_logger(__name__)
MAGIC_NC_DATASET_NAME = 'Automated NC import'


@app.task
def download_and_import_nc_dataset():
    """
    This task is responsible for automatically downloading
    and importing the latest NC data.  It does this by
    setting up a Dataset model instance appropriately then
    triggering a download task (as if an admin had triggered
    it manually).
    """
    logger.info('Triggering automatic NC import')
    Dataset.objects.filter(name=MAGIC_NC_DATASET_NAME).delete()
    if os.path.exists(settings.NC_AUTO_IMPORT_DIRECTORY):
        logger.info('Cleaning up download directory %s',
                    settings.NC_AUTO_IMPORT_DIRECTORY)
        shutil.rmtree(settings.NC_AUTO_IMPORT_DIRECTORY)
    nc_dataset = Dataset(
        state=settings.NC_KEY,
        name=MAGIC_NC_DATASET_NAME,
        # NC data export updated nightly around 10:30 p.m. Eastern
        date_received=now().date() - timedelta(days=1),
        url=MAGIC_NC_FTP_URL,
        destination=settings.NC_AUTO_IMPORT_DIRECTORY,
    )
    if len(settings.NC_AUTO_IMPORT_MONITORS) >= 1:
        nc_dataset.report_email_1 = settings.NC_AUTO_IMPORT_MONITORS[0]
    if len(settings.NC_AUTO_IMPORT_MONITORS) >= 2:
        nc_dataset.report_email_2 = settings.NC_AUTO_IMPORT_MONITORS[1]
    nc_dataset.save()
    import_dataset.delay(nc_dataset.pk)
