from django.conf import settings
import djclick as click

from nc.models import Agency, Search, Stop
from tsdata.dataset_facts import compute_dataset_facts


@click.command()
def command():
    facts = compute_dataset_facts(Agency, Stop, settings.NC_TIME_ZONE, Search=Search)
    for fact in facts:
        click.secho(fact)
