import csv
import datetime
import io

from celery.utils.log import get_task_logger

from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.db.models import Max, Q
from django.utils import timezone

from il.data.importer import run as il_run
from md.data.importer import run as md_run
from nc.data.importer import run as nc_run
from traffic_stops.celery import app
from tsdata.models import Dataset, Import


logger = get_task_logger(__name__)

RUN_MAP = {
    settings.IL_KEY: il_run,
    settings.MD_KEY: md_run,
    settings.NC_KEY: nc_run,
}


@app.task
def import_dataset(dataset_id):
    """Execute a state dataset import process"""
    logger.info("Received Dataset ID: {}".format(dataset_id))
    dataset = Dataset.objects.get(pk=dataset_id)
    run = Import.objects.create(dataset=dataset)
    logger.info("Starting {} import".format(dataset.state))
    state_import = RUN_MAP[run.dataset.state]
    report_emails = [
        email for email in [dataset.report_email_1, dataset.report_email_2]
        if email
    ]
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
    if report_emails:
        send_mail(
            'Import completed successfully',
            'Import of %s completed successfully' % dataset,
            settings.DEFAULT_FROM_EMAIL,
            report_emails,
        )

    compliance_report.delay(dataset_id)


@app.task
def compliance_report(dataset_id):
    if not settings.COMPLIANCE_REPORT_LIST:
        return

    dataset = Dataset.objects.get(pk=dataset_id)
    if dataset.state != settings.NC_KEY:
        return

    Agency = dataset.agency_model

    now = timezone.now()
    qs = Agency.objects.annotate(
        last_reported=Max('stops__date')
    ).filter(
        Q(last_reported__lt=now - datetime.timedelta(days=90)) |
        Q(last_reported__isnull=True)
    ).values(
        'id', 'name', 'last_reported'
    ).order_by('-last_reported')

    if not qs:
        send_mail(
            "{} Compliance Report, {}".format(dataset.state.upper(), now.date().isoformat()),
            "All agencies have reported within the last 90 days.",
            settings.DEFAULT_FROM_EMAIL,
            settings.COMPLIANCE_REPORT_LIST
        )
        return

    csvfile = io.StringIO()
    writer = csv.DictWriter(csvfile, fieldnames=('id', 'name', 'last_reported'))
    writer.writeheader()
    writer.writerows(filter(lambda r: r['last_reported'] is not None, qs))
    # Sort the agencies with no stops reported last
    writer.writerows(filter(lambda r: r['last_reported'] is None, qs))

    message = EmailMessage(
        "{} Compliance Report, {}".format(dataset.state.upper(), now.date().isoformat()),
        "Attached are the agencies out of compliance in the most recent data import.",
        settings.DEFAULT_FROM_EMAIL,
        settings.COMPLIANCE_REPORT_LIST
    )
    message.attach('report.csv', csvfile.getvalue(), 'text/csv')
    message.send()
