from django.db import models

class Crew(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Pirate(models.Model):
    name = models.CharField(max_length=128)
    bounty = models.IntegerField(null=True)
    crew = models.ForeignKey(Crew, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name
