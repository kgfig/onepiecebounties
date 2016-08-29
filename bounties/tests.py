from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from . import views
from .models import Crew, Pirate

class CrewModelTest(TestCase):

    def test_model_save_and_retrieve_crew(self):
        crew = Crew(name='Straw Hat Crew')
        crew.save()
        
        result = Crew.objects.first()
        self.assertEqual(result, crew)

class PirateModelTest(TestCase):

    def test_model_save_and_retrieve_pirate_without_bounty(self):
        big_mom = Pirate(name='Charlotte Linlin')
        big_mom.save()
        
        first = Pirate.objects.first()
        self.assertEqual(first, big_mom)
        
    def test_model_save_and_retrieve_pirate_bounty(self):
        luffy = Pirate(name='Monkey D. Luffy', bounty=500000000)
        luffy.save()
        
        first = Pirate.objects.first()
        self.assertEqual(first.bounty, luffy.bounty)

    def test_model_save_and_retrieve_pirate_with_crew(self):
        strawhat = Crew(name='Straw Hat Crew')
        strawhat.save()
        
        luffy = Pirate(name='Monkey D. Luffy', bounty=500000000)
        luffy.crew = strawhat
        luffy.save()

        result = Pirate.objects.first()
        self.assertEqual(result.crew, strawhat)

    def test_model_search_pirate_whose_name_exactly_matches_keyword(self):
        luffy = Pirate(name='Monkey D. Luffy')
        luffy.save()
        
        alvida = Pirate(name='Iron Mace Alvida')
        alvida.save()

        result = Pirate.objects.get(name='Monkey D. Luffy')
        self.assertEqual(result, luffy)

    def test_model_returns_pirates_with_matching_names(self):
        luffy = Pirate(name='Monkey D. Luffy')
        luffy.save()
        hancock = Pirate(name='Boa Hancock')
        hancock.save()
        marigold = Pirate(name='Boa Marigold')
        marigold.save()
        
        result = Pirate.objects.filter(name__icontains='Boa')
        self.assertEqual(result.count(), 2)
        
    def test_model_should_not_return_pirate_not_matching_query(self):
        luffy = Pirate(name='Monkey D. Luffy')
        luffy.save()
        hancock = Pirate(name='Boa Hancock')
        hancock.save()

        result = Pirate.objects.filter(name__icontains='Luffy')
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
        luffy = Pirate(name='Monkey D. Luffy')
        luffy.save()
        alvida = Pirate(name='Iron Mace Alvida')
        alvida.save()
        shanks = Pirate(name='Red-Haired Shanks')
        shanks.save()
        
        response = self.client.get(reverse('bounties:index'))
        context = response.context['pirates']
        
        self.assertEqual(context.get(id=1), luffy)
        self.assertEqual(context.get(id=2), alvida)
        self.assertEqual(context.get(id=3), shanks)

    def test_template_has_all_pirate_names_in_suggestions(self):
        luffy = Pirate(name='Monkey D. Luffy')
        luffy.save()
        alvida = Pirate(name='Iron Mace Alvida')
        alvida.save()
        shanks = Pirate(name='Red-Haired Shanks')
        shanks.save()
        
        response = self.client.get(reverse('bounties:index'))
        self.assertContains(response, luffy.name)
        self.assertContains(response, alvida.name)
        self.assertContains(response, shanks.name)

    '''
    If user searches for "Monkey D. Luffy" and no pirate name
    contains the keyword, the user should not be redirected.
    '''
    def test_view_goes_to_index_if_no_matching_pirate(self):
        alvida = Pirate(name='Iron Mace Alvida')
        alvida.save()
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field': 'Monkey D. Luffy'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    '''
    If there is an exact match for the user's search keyword,
    the user should be redirected to that pirate's info page
    '''
    def test_view_redirects_to_profile_of_matching_pirate(self):
        alvida = Pirate(name='Iron Mace Alvida')
        alvida.save()
        luffy = Pirate(name='Monkey D. Luffy')
        luffy.save()
        
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field': luffy.name})
        self.assertRedirects(response, reverse('bounties:get_pirate', kwargs={'pirate_id': luffy.id,}))

    '''
    If there is more than one pirate whose name matches the keyword,
    the user should go to the home page with the results.
    '''
    def test_view_go_to_home_page_and_display_multiple_search_results(self):
        hancock = Pirate(name='Boa Hancock')
        hancock.save()
        marigold = Pirate(name='Boa Marigold')
        marigold.save()

        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field': 'Boa'})
        # TODO replace with assertions for search results
        self.assertContains(response, '<option value="%s">%s</option>' % (hancock.name, hancock.name,), html=True)
        self.assertContains(response, '<option value="%s">%s</option>' % (marigold.name, marigold.name,), html=True)

    '''
    If there are pirates whose names contain the keyword,
    the results should NOT contain the other pirates whose names don't match the query.
    '''
    def test_view_search_should_not_include_pirates_not_matching_query(self):
        luffy = Pirate(name='Monkey D. Luffy')
        luffy.save()
        hancock = Pirate(name='Boa Hancock')
        hancock.save()
        marigold = Pirate(name='Boa Marigold')
        marigold.save()

        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field':'Boa'})
        self.assertNotContains(response, luffy.name)

class GetPirateTest(TestCase):

    def test_url_resolves_to_get_pirate_view(self):
        pirate = Pirate(name='Monkey D. Luffy')
        pirate.save()
        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id':1}))
        self.assertEqual(response.resolver_match.func, views.get_pirate)

    def test_view_returns_matching_pirate(self):
        alvida = Pirate(name='Iron Mace Alvida')
        alvida.save()
        luffy = Pirate(name='Monkey D. Luffy')
        luffy.save()

        result = Pirate.objects.get(name='Monkey D. Luffy')
        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': result.id,}))
        self.assertContains(response, result.name)

    def test_view_returns_profile_template(self):
        pirate = Pirate(name='Monkey D. Luffy')
        pirate.save()
        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': pirate.id,}))
        self.assertTemplateUsed(response, 'profile.html')

    def test_view_shows_pirate_bounty(self):
        pirate = Pirate(name='Monkey D. Luffy', bounty=500000000)
        pirate.save()
        formatted_bounty = '{:,}'.format(pirate.bounty)
        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': pirate.id,}))
        self.assertContains(response, formatted_bounty)

    def test_view_shows_pirate_crew(self):
        crew = Crew(name='Straw Hat Crew')
        crew.save()
        pirate = Pirate(name='Monkey D. Luffy', bounty=500000000, crew=crew)
        pirate.save()

        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': pirate.id,}))
        self.assertContains(response, crew.name)

    def test_view_passes_complete_pirate_context_to_template(self):
        crew = Crew(name='Heart Pirates')
        crew.save()
        pirate = Pirate(name='Trafalgar D. Law', bounty=500000000, crew=crew)
        pirate .save()

        response = self.client.get(reverse('bounties:get_pirate', kwargs={'pirate_id': pirate.id,}))
        pirate_context = response.context['pirate']
        self.assertEqual(pirate_context, pirate)
