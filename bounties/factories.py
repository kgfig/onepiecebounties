from factory import DjangoModelFactory, lazy_attribute, SubFactory
from . import models

class Crew(DjangoModelFactory):
    class Meta:
        model = models.Crew
        django_get_or_create = ('name',)

    name = 'Straw Hat Crew'

class Pirate(DjangoModelFactory):
    class Meta:
        model = models.Pirate
        django_get_or_create = ('name',)
        
    name = 'Monkey D. Luffy'
    bounty = 500000000
    crew = SubFactory(Crew)
    
