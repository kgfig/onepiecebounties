from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.template.defaultfilters import slugify
from bounties import factories, views
from bounties.models import Crew, Pirate

class ListTemplateTest(TestCase):

    def test_should_not_include_pirates_not_matching_query(self):
        luffy = factories.Pirate()
        handcock = factories.Pirate(name='Boa Hancock', bounty=None, crew=None)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=None)
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field':'Boa'})
        
        luffy_url = reverse('bounties:get_pirate', kwargs={'pirate_id': luffy.id,})
        self.assertNotContains(response, '<a href="%s">' % (luffy_url,))

    def test_shows_links_to_matching_pirates(self):
        hancock = factories.Pirate(name='Boa Hancock', bounty=None, crew=None)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=None)
        hancock_url = reverse('bounties:get_pirate', kwargs={'pirate_id': hancock.id,})
        marigold_url = reverse('bounties:get_pirate', kwargs={'pirate_id': marigold.id,})
        
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field':'Boa'})
        self.assertContains(response, '<a href="%s">' % (hancock_url,))
        self.assertContains(response, '<a href="%s">' % (marigold_url,))

    def test_shows_crew_of_matching_pirates(self):
        crew = factories.Crew(name='Kuja Pirates')
        hancock = factories.Pirate(name='Boa Hancock', bounty=None, crew=crew)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=crew)
        
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field':'Boa'})
        self.assertContains(response, crew.name.upper())

    def test_shows_image_of_matching_pirates(self):
        hancock = factories.Pirate(name='Boa Hancock', bounty=None, crew=None)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=None)

        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field': 'Boa'})
        hancock_url = static('images/pirates/%s' % (hancock.filename(),))
        marigold_url = static('images/pirates/%s' % (marigold.filename(),))
        self.assertContains(response, hancock_url)
        self.assertContains(response, marigold_url)

    def test_shows_wanted_status_of_matching_pirates(self):
        crew = factories.Crew()
        luffy = factories.Pirate(name='Test Luffy', wanted_status=Pirate.DEAD_OR_ALIVE)
        sanji = factories.Pirate(name='Test Sanji', bounty=177000000, crew=crew, wanted_status=Pirate.ONLY_ALIVE)

        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field': 'Test'})
        self.assertContains(response, luffy.get_wanted_status_display().upper())
        self.assertContains(response, sanji.get_wanted_status_display().upper())
