from django.conf import settings
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.template.defaultfilters import slugify
from bounties import factories, views
from bounties.models import Crew, Pirate

class GetPirateTest(TestCase):

    def test_url_resolves_to_get_pirate_view(self):
        luffy = factories.Pirate()
        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id':1}))
        self.assertEqual(response.resolver_match.func, views.get_pirate)

    def test_view_returns_matching_pirate(self):
        alvida = factories.Pirate(name='Iron Mace Alvida', bounty=None, crew=None)
        luffy = factories.Pirate()
        result = Pirate.objects.get(name='Monkey D. Luffy')
        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': result.id,}))
        self.assertContains(response, result.name)

    def test_view_returns_profile_template(self):
        pirate = factories.Pirate()
        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': pirate.id,}))
        self.assertTemplateUsed(response, 'profile.html')

    def test_view_passes_complete_pirate_context_to_template(self):
        crew = factories.Crew(name='Heart Pirates')
        pirate = factories.Pirate(name='Trafalgar D. Law', bounty=500000000, crew=crew)
        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': pirate.id,}))
        pirate_context = response.context['pirate']
        self.assertEqual(pirate_context, pirate)

    def test_view_passes_list_of_pirates_context_to_template(self):
        hancock = factories.Pirate(name='Boa Hancock', bounty=None, crew=None)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=None)
        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': hancock.id,}))
        list_context = response.context['pirates']
        self.assertIn(hancock, list_context)

    def test_template_shows_pirate_bounty(self):
        pirate = factories.Pirate()
        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': pirate.id,}))
        self.assertContains(response, pirate.formatted_bounty())

    def test_template_shows_pirate_crew(self):
        crew = factories.Crew()
        pirate = factories.Pirate(crew=crew)
        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': pirate.id,}))
        self.assertContains(response, crew.name)

    def test_template_has_correct_pirate_image(self):
        pirate = factories.Pirate()
        other_pirate = factories.Pirate(name='Tony Tony Chopper', bounty=100)
        
        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': pirate.id,}))
        self.assertContains(response, pirate.filename())

        new_response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': other_pirate.id,}))
        self.assertContains(new_response, other_pirate.filename())

    def test_template_does_not_show_bounty_if_pirate_has_no_bounty(self):
        no_bounty_pirate = factories.Pirate(bounty=None)
        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': no_bounty_pirate.id,}))
        self.assertNotContains(response, '<p class="bounty">', html=True)

    def test_template_shows_wanted_status(self):
        pirate = factories.Pirate(wanted_status=Pirate.DEAD_OR_ALIVE)
        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': pirate.id,}))
        self.assertContains(response, pirate.get_wanted_status_display())
    
    # TODO Find a way to do this
    #def test_view_image_url_is_accessible(self):
    #    pirate = factories.Pirate()
    #    # TODO get static url using a better way
    #    image_url = '%simages/pirates/%s%s' % (settings.STATIC_URL, pirate.filename(), ".png",)
    #    response = self.client.get(image_url)
    #    print(image_url)
    #    self.assertEqual(response.status_code, 200)
