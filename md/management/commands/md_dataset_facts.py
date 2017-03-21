from django.conf import settings
import djclick as click

from md.models import Agency, Stop
from tsdata.dataset_facts import compute_dataset_facts


@click.command()
def command():
    facts = compute_dataset_facts(Agency, Stop, settings.MD_KEY)
    for fact in facts:
        click.echo(fact)
