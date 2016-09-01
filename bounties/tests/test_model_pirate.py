from django.conf import settings
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.template.defaultfilters import slugify
from bounties import factories
from bounties.models import Crew, Pirate

class PirateModelTest(TestCase):

    def save_and_retrieve_pirate_without_bounty(self):
        pirate_no_bounty = factories.Pirate(bounty=None)
        first = Pirate.objects.first()
        self.assertEqual(first, pirate_no_bounty)
        
    def save_and_retrieve_pirate_bounty_without_crew(self):
        pirate_with_bounty = factories.Pirate(crew=None)
        result = Pirate.objects.first()
        self.assertEqual(result.bounty, pirate_with_bounty.bounty)

    def save_and_retrieve_pirate_with_crew(self):
        crew = factories.Crew()
        pirate = factories.Pirate(crew=crew)
        result = Pirate.objects.first()
        self.assertEqual(result.crew, crew)

    def search_pirate_whose_name_exactly_matches_keyword(self):
        luffy = factories.Pirate()
        alvida = factories.Pirate(name='Iron Mace Alvida', bounty=None, crew=None)
        result = Pirate.objects.get(name=luffy.name)
        self.assertEqual(result, luffy)

    def returns_pirates_with_matching_names(self):
        luffy = factories.Pirate()
        hancock = factories.Pirate(name='Boa Hancock', bounty=None, crew=None)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=None)
        result = Pirate.objects.filter(name__icontains='Boa')
        self.assertEqual(result.count(), 2)
        
    def should_not_return_pirate_not_matching_query(self):
        luffy = factories.Pirate()
        hancock = factories.Pirate(name='Boa Hancock', bounty=None, crew=None)
        result = Pirate.objects.filter(name__icontains='Boa')
        self.assertEqual(result.count(), 1)

    def should_return_slugified_name_as_filename(self):
        pirate = factories.Pirate()
        correct_filename = slugify(pirate.name)
        self.assertEqual(pirate.filename(), correct_filename)

    def returns_formatted_bounty_with_comma(self):
        pirate = factories.Pirate(bounty=500000000)
        formatted_bounty = '500,000,000'
        self.assertEqual(pirate.formatted_bounty(), formatted_bounty)

    def formatted_bounty_returns_None_if_no_bounty(self):
        pirate = factories.Pirate(bounty=None)
        self.assertIsNone(pirate.formatted_bounty())
