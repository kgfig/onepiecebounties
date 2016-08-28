from django.core.urlresolvers import resolve
from django.test import TestCase
from .views import index
from .models import Pirate

class PirateModelTest(TestCase):

    def test_model_save_and_retrieve_pirates(self):
        luffy = Pirate(name='Monkey D. Luffy')
        luffy.save()
        
        first = Pirate.objects.first()
        self.assertEqual(first.name, luffy.name)
        
    def test_model_can_save_and_retrieve_multiple_pirates(self):
        luffy = Pirate(name='Monkey D. Luffy')
        luffy.save()
        
        alvida = Pirate(name='Iron Mace Alvida')
        alvida.save()

        pirates = Pirate.objects.all()
        self.assertEqual(pirates.count(), 2)

    def test_model_can_search_pirate_whose_name_exactly_matches_keyword(self):
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
        found = resolve('/onepiecebounties/')
        self.assertEqual(found.func, index)

    def test_template_returns_home_template(self):
        response = self.client.get('/onepiecebounties/')
        self.assertTemplateUsed(response, 'index.html')

    def test_view_returns_OK(self):
        response = self.client.get('/onepiecebounties/')
        self.assertEqual(response.status_code, 200)

    def test_view_passes_correct_context_to_template(self):
        luffy = Pirate(name='Monkey D. Luffy')
        luffy.save()
        alvida = Pirate(name='Iron Mace Alvida')
        alvida.save()
        shanks = Pirate(name='Red-Haired Shanks')
        shanks.save()
        
        response = self.client.get('/onepiecebounties/')
        context = response.context['pirates']
        
        self.assertEqual(context.get(id=1), luffy)
        self.assertEqual(context.get(id=2), alvida)
        self.assertEqual(context.get(id=3), shanks)

    def test_template_shows_all_pirates(self):
        luffy = Pirate(name='Monkey D. Luffy')
        luffy.save()
        alvida = Pirate(name='Iron Mace Alvida')
        alvida.save()
        shanks = Pirate(name='Red-Haired Shanks')
        shanks.save()
        
        response = self.client.get('/onepiecebounties/')
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
        response = self.client.get('/onepiecebounties/', data={'pirate-search-field': 'Monkey D. Luffy'})
        self.assertEqual(response.status_code, 200)

    '''
    If there is an exact match for the user's search keyword,
    the user should be redirected to that pirate's info page
    '''
    def test_view_redirects_to_profile_of_matching_pirate(self):
        alvida = Pirate(name='Iron Mace Alvida')
        alvida.save()
        luffy = Pirate(name='Monkey D. Luffy')
        luffy.save()
        
        response = self.client.get('/onepiecebounties/', data={'pirate-search-field': luffy.name})
        self.assertRedirects(response, '/onepiecebounties/%d/' % (luffy.id,))

    '''
    If there is more than one pirate whose name matches the keyword,
    the user should go to the home page with the results.
    '''
    def test_view_go_to_home_page_and_display_multiple_search_results(self):
        hancock = Pirate(name='Boa Hancock')
        hancock.save()
        marigold = Pirate(name='Boa Marigold')
        marigold.save()

        response = self.client.get('/onepiecebounties/', data={'pirate-search-field': 'Boa'})
        self.assertContains(response, hancock.name)
        self.assertContains(response, marigold.name)

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

        response = self.client.get('/onepiecebounties/', data={'pirate-search-field':'Boa'})
        self.assertNotContains(response, luffy.name)

class GetPirateTest(TestCase):

    def test_view_returns_matching_pirate(self):
        alvida = Pirate(name='Iron Mace Alvida')
        alvida.save()
        luffy = Pirate(name='Monkey D. Luffy')
        luffy.save()

        result = Pirate.objects.get(name='Monkey D. Luffy')
        response = self.client.get('/onepiecebounties/%d/' % (result.id,))
        self.assertContains(response, result.name)

    def test_view_returns_profile_template(self):
        luffy = Pirate(name='Monkey D. Luffy')
        luffy.save()
        response = self.client.get('/onepiecebounties/%d/' % (luffy.id,))
        self.assertTemplateUsed(response, 'profile.html')
