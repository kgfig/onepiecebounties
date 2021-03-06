from django.conf import settings
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.template.defaultfilters import slugify
from bounties import factories
from bounties.models import Crew, Pirate

class CrewModelTest(TestCase):

    def test_str_should_return_name(self):
        crew = Crew(name='Whitebeard Pirates')
        self.assertEqual(crew.__str__(), crew.name)

    def test_model_save_and_retrieve_crew(self):
        crew = factories.Crew()
        result = Crew.objects.first()
        self.assertEqual(result, crew)
