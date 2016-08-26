from django.db import models

class Pirate(models.Model):
    name = models.CharField(max_length=128)
