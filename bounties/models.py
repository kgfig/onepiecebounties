from django.db import models
from django.template.defaultfilters import slugify

class Crew(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Pirate(models.Model):
    DEAD_OR_ALIVE = 1
    ONLY_ALIVE = 2
    
    STATUS_CHOICES = (
        (DEAD_OR_ALIVE, 'Dead or Alive'),
        (ONLY_ALIVE, 'Only Alive'),
    )
    
    name = models.CharField(max_length=128)
    bounty = models.IntegerField(null=True)
    crew = models.ForeignKey(Crew, on_delete=models.SET_NULL, blank=True, null=True)
    wanted_status = models.IntegerField(choices=STATUS_CHOICES, default=DEAD_OR_ALIVE)

    def filename(self):
        return slugify(self.name)

    def formatted_bounty(self):
        return '{:,}'.format(self.bounty) if self.bounty else None

    def __str__(self):
        return self.name
