from django.db import models


STATE_CHOICES = (
    ('nc', 'North Carolina'),
    ('md', 'Maryland'),
    ('il', 'Illinois'),
)

STATUS_CHOICES = (
    ('running', 'Running'),
    ('error', 'Error'),
    ('finished', 'Finished'),
)

GEOGRAPY_CHOICES = (
    ('county', 'County'),
    ('place', 'Place'),
)


class Dataset(models.Model):
    state = models.CharField(choices=STATE_CHOICES, max_length=2)
    name = models.CharField(max_length=255, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_received = models.DateField()
    url = models.URLField("URL", unique=True)
    destination = models.CharField(blank=True, max_length=1024,
                                   help_text="Absolute path to destination directory (helpful for testing)")  # noqa

    def __str__(self):
        return "{}: {}".format(self.get_state_display(), self.name)


class Import(models.Model):
    dataset = models.ForeignKey(Dataset)
    date_started = models.DateTimeField(auto_now_add=True)
    date_finished = models.DateTimeField(null=True)
    successful = models.BooleanField(default=False)

    def __str__(self):
        return 'Import of {}'.format(self.dataset)


class CensusProfile(models.Model):
    id = models.CharField("ID", primary_key=True, max_length=16)
    location = models.CharField(max_length=255)
    geography = models.CharField(max_length=16, choices=GEOGRAPY_CHOICES)
    state = models.CharField(max_length=2)
    source = models.CharField(max_length=255)
    white = models.PositiveIntegerField(default=0)
    black = models.PositiveIntegerField(default=0)
    native_american = models.PositiveIntegerField(default=0)
    asian = models.PositiveIntegerField(default=0)
    native_hawaiian = models.PositiveIntegerField(default=0)
    other = models.PositiveIntegerField(default=0)
    two_or_more_races = models.PositiveIntegerField(default=0)
    hispanic = models.PositiveIntegerField(default=0)
    non_hispanic = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.location

    def get_census_dict(self):
        return dict(
            white=self.white,
            black=self.black,
            native_american=self.native_american,
            asian=self.asian,
            other=self.other + self.native_hawaiian + self.two_or_more_races,
            hispanic=self.hispanic,
            non_hispanic=self.non_hispanic,
            total=self.total,
        )
