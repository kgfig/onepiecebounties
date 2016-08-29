from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from . import factories, views
from .models import Crew, Pirate

class CrewModelTest(TestCase):

    def test_model_save_and_retrieve_crew(self):
        crew = factories.Crew()
        result = Crew.objects.first()
        self.assertEqual(result, crew)

class PirateModelTest(TestCase):

    def test_model_save_and_retrieve_pirate_without_bounty(self):
        pirate_no_bounty = factories.Pirate(bounty=None)
        first = Pirate.objects.first()
        self.assertEqual(first, pirate_no_bounty)
        
    def test_model_save_and_retrieve_pirate_bounty_without_crew(self):
        pirate_with_bounty = factories.Pirate(crew=None)
        result = Pirate.objects.first()
        self.assertEqual(result.bounty, pirate_with_bounty.bounty)

    def test_model_save_and_retrieve_pirate_with_crew(self):
        crew = factories.Crew()
        pirate = factories.Pirate(crew=crew)
        result = Pirate.objects.first()
        self.assertEqual(result.crew, crew)

    def test_model_search_pirate_whose_name_exactly_matches_keyword(self):
        luffy = factories.Pirate()
        alvida = factories.Pirate(name='Iron Mace Alvida', bounty=None, crew=None)
        result = Pirate.objects.get(name=luffy.name)
        self.assertEqual(result, luffy)

    def test_model_returns_pirates_with_matching_names(self):
        luffy = factories.Pirate()
        hancock = factories.Pirate(name='Boa Hancock', bounty=None, crew=None)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=None)
        result = Pirate.objects.filter(name__icontains='Boa')
        self.assertEqual(result.count(), 2)
        
    def test_model_should_not_return_pirate_not_matching_query(self):
        luffy = factories.Pirate()
        hancock = factories.Pirate(name='Boa Hancock', bounty=None, crew=None)
        result = Pirate.objects.filter(name__icontains='Boa')
        self.assertEqual(result.count(), 1)

class IndexPageTest(TestCase):

    def test_url_can_resolve_to_home_page_view(self):
        response = self.client.get(reverse('bounties:index'))
        self.assertEqual(response.resolver_match.func, views.index)

    def test_template_returns_home_template(self):
        response = self.client.get(reverse('bounties:index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_view_returns_OK(self):
        response = self.client.get(reverse('bounties:index'))
        self.assertEqual(response.status_code, 200)

    def test_view_passes_correct_context_to_template(self):
        luffy = factories.Pirate()
        alvida = factories.Pirate(name='Iron Mace Alvida', bounty=None, crew=None)
        shanks = factories.Pirate(name='Red-Haired Shanks', bounty=None, crew=None)
        
        response = self.client.get(reverse('bounties:index'))
        context = response.context['pirates']
        
        self.assertEqual(context.get(id=1), luffy)
        self.assertEqual(context.get(id=2), alvida)
        self.assertEqual(context.get(id=3), shanks)

    def test_template_has_all_pirate_names_in_suggestions(self):
        luffy = factories.Pirate()
        alvida = factories.Pirate(name='Iron Mace Alvida', bounty=None, crew=None)
        shanks = factories.Pirate(name='Red-Haired Shanks', bounty=None, crew=None)
        response = self.client.get(reverse('bounties:index'))
        self.assertContains(response, '<option value="%s">%s</option>' % (luffy.name, luffy.name,), html=True)
        self.assertContains(response, '<option value="%s">%s</option>' % (alvida.name, alvida.name,), html=True)
        self.assertContains(response, '<option value="%s">%s</option>' % (shanks.name, shanks.name,), html=True)

    # If user searches for "Monkey D. Luffy" and no pirate name
    # contains the keyword, the user should not be redirected.
    def test_view_goes_to_index_if_no_matching_pirate(self):
        alvida = factories.Pirate(name='Iron Mace Alvida', bounty=None, crew=None)
        alvida.save()
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field': 'Monkey D. Luffy'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    # If there is an exact match for the user's search keyword,
    # the user should be redirected to that pirate's info page
    def test_view_redirects_to_profile_of_matching_pirate(self):
        luffy = factories.Pirate()
        alvida = factories.Pirate(name='Iron Mace Alvida', bounty=None, crew=None)
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field': luffy.name})
        self.assertRedirects(response, reverse('bounties:get_pirate', kwargs={'pirate_id': luffy.id,}))

    # If there is more than one pirate whose name matches the keyword,
    # the user should go to the home page with the results.
    def test_view_go_to_home_page_and_display_multiple_search_results(self):
        handcock = factories.Pirate(name='Boa Hancock', bounty=None, crew=None)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=None)
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field': 'Boa'})
        # TODO for search results
        # self.assertContains(response, '<a href="%s">%s</a>' % (reverse('bounties:get_pirate', kwargs={'pirate_id':hancock.id}), hancock.name,), html=True)
        # self.assertContains(response, '<a href="%s">%s</a>' % (reverse('bounties:get_pirate', kwargs={'pirate_id':marigold.id}), marigold.name,), html=True)

    # If there are pirates whose names contain the keyword,
    # the results should NOT contain the other pirates whose names don't match the query.
    def test_view_search_should_not_include_pirates_not_matching_query(self):
        luffy = factories.Pirate()
        handcock = factories.Pirate(name='Boa Hancock', bounty=None, crew=None)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=None)
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field':'Boa'})
        self.assertNotContains(response, luffy.name)

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

    def test_view_shows_pirate_bounty(self):
        pirate = factories.Pirate()
        formatted_bounty = '{:,}'.format(pirate.bounty)
        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': pirate.id,}))
        self.assertContains(response, formatted_bounty)

    def test_view_shows_pirate_crew(self):
        crew = factories.Crew()
        pirate = factories.Pirate(crew=crew)
        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': pirate.id,}))
        self.assertContains(response, crew.name)

    def test_view_passes_complete_pirate_context_to_template(self):
        crew = factories.Crew(name='Heart Pirates')
        pirate = factories.Pirate(name='Trafalgar D. Law', bounty=500000000, crew=crew)
        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': pirate.id,}))
        pirate_context = response.context['pirate']
        self.assertEqual(pirate_context, pirate)
