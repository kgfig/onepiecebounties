from django.db import models

class Pirate(models.Model):
    name = models.CharField(max_length=128)
    bounty = models.IntegerField(null=True)

    def __str__(self):
        return self.name
