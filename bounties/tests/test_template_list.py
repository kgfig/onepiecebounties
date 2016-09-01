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
        self.assertNotContains(response, '<a href="%s">%s</a>' % (luffy_url, luffy.name,), html=True)

    def test_shows_links_to_matching_pirates(self):
        hancock = factories.Pirate(name='Boa Hancock', bounty=None, crew=None)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=None)
        hancock_url = reverse('bounties:get_pirate', kwargs={'pirate_id': hancock.id,})
        marigold_url = reverse('bounties:get_pirate', kwargs={'pirate_id': marigold.id,})
        
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field':'Boa'})
        self.assertContains(response, '<a href="%s">%s</a>' % (hancock_url, hancock.name,), html=True)
        self.assertContains(response, '<a href="%s">%s</a>' % (marigold_url, marigold.name,), html=True)

    def test_shows_crew_of_matching_pirates(self):
        crew = factories.Crew(name='Kuja Pirates')
        hancock = factories.Pirate(name='Boa Hancock', bounty=None, crew=crew)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=crew)
        
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field':'Boa'})
        self.assertContains(response, crew.name)

    def test_shows_crew_of_matching_pirates(self):
        crew = factories.Crew(name='Kuja Pirates')
        hancock = factories.Pirate(name='Boa Hancock', bounty=None, crew=crew)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=crew)
        
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field':'Boa'})
        self.assertContains(response, crew.name)

    def test_shows_bounty_of_matching_pirates(self):
        whitebeard = factories.Crew(name='Whitebeard Pirates')
        luffy = factories.Pirate(bounty=500000000)
        ace = factories.Pirate(name='Portgas D. Ace', bounty=None, crew=whitebeard)
        
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field': 'D.'})
        self.assertContains(response, luffy.formatted_bounty())
        
    def test_no_bounty_in_page_if_matching_pirate_has_no_bounty(self):
        whitebeard = factories.Crew(name='Whitebeard Pirates')
        pretimeskip_luffy = factories.Pirate(bounty=100000000)
        ace = factories.Pirate(name='Portgas D. Ace', bounty=None, crew=whitebeard)
        
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field': 'D.'})
        self.assertNotContains(response, 'None')
        
    def test_shows_image_of_matching_pirates(self):
        hancock = factories.Pirate(name='Boa Hancock', bounty=None, crew=None)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=None)

        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field': 'Boa'})
        hancock_url = static('images/pirates/%s.png' % (hancock.filename(),))
        marigold_url = static('images/pirates/%s.png' % (marigold.filename(),))
        self.assertContains(response, hancock_url)
        self.assertContains(response, marigold_url)
