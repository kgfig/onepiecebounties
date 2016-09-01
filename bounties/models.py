from django.db import models
from django.template.defaultfilters import slugify

class Crew(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Pirate(models.Model):
    name = models.CharField(max_length=128)
    bounty = models.IntegerField(null=True)
    crew = models.ForeignKey(Crew, on_delete=models.SET_NULL, blank=True, null=True)

    def filename(self):
        return slugify(self.name)

    def formatted_bounty(self):
        return '{:,}'.format(self.bounty)

    def __str__(self):
        return self.name
