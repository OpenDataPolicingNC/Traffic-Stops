from django.db import models


STATE_CHOICES = (
    ('nc', 'North Carolina'),
    ('md', 'Maryland'),
)

STATUS_CHOICES = (
    ('running', 'Running'),
    ('error', 'Error'),
    ('finished', 'Finished'),
)


class Dataset(models.Model):
    state = models.CharField(choices=STATE_CHOICES, max_length=2)
    name = models.CharField(max_length=255, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_received = models.DateField()
    url = models.URLField("URL", unique=True)
    destination = models.CharField(blank=True, max_length=1024,
                                   help_text="Absolute path to destination directory (helpful for testing)")

    def __str__(self):
        return "{}: {}".format(self.get_state_display(), self.name)


class Import(models.Model):
    dataset = models.ForeignKey(Dataset)
    date_started = models.DateTimeField(auto_now_add=True)
    date_finished = models.DateTimeField(null=True)
    successful = models.BooleanField(default=False)
