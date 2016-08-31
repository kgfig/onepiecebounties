from django.conf import settings
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.template.defaultfilters import slugify
from bounties import factories, views
from bounties.models import Crew, Pirate

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

    def test_view_goes_to_home_page_and_displays_multiple_search_results(self):
        handcock = factories.Pirate(name='Boa Hancock', bounty=None, crew=None)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=None)
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field': 'Boa'})
        

    # If there is more than one pirate whose name matches the keyword,
    # the user should go to the home page with the results.
    def test_view_returns_list_template_if_there_are_multiple_search_results(self):
        handcock = factories.Pirate(name='Boa Hancock', bounty=None, crew=None)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=None)
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field': 'Boa'})
        self.assertTemplateUsed(response, 'list.html')
        
        # TODO for search results
        # self.assertContains(response, '<a href="%s">%s</a>' % (reverse('bounties:get_pirate', kwargs={'pirate_id':hancock.id}), hancock.name,), html=True)
        # self.assertContains(response, '<a href="%s">%s</a>' % (reverse('bounties:get_pirate', kwargs={'pirate_id':marigold.id}), marigold.name,), html=True)
        
    # If there are pirates whose names contain the keyword,
    # the results should NOT contain the other pirates whose names don't match the query.
    def test_view_should_not_include_pirates_not_matching_query_in_list_template(self):
        luffy = factories.Pirate()
        handcock = factories.Pirate(name='Boa Hancock', bounty=None, crew=None)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=None)
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field':'Boa'})
        luffy_url = reverse('bounties:get_pirate', kwargs={'pirate_id': luffy.id,})
        self.assertNotContains(response, '<a href="%s">%s</a>' % (luffy_url, luffy.name,), html=True)

    def test_view_shows_matching_pirates_in_list_template(self):
        hancock = factories.Pirate(name='Boa Hancock', bounty=None, crew=None)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=None)
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field':'Boa'})
        hancock_url = reverse('bounties:get_pirate', kwargs={'pirate_id': hancock.id,})
        marigold_url = reverse('bounties:get_pirate', kwargs={'pirate_id': marigold.id,})
        self.assertContains(response, '<a href="%s">%s</a>' % (hancock_url, hancock.name,), html=True)
        self.assertContains(response, '<a href="%s">%s</a>' % (marigold_url, marigold.name,), html=True)

    def test_view_passes_correct_list_context_to_results_list_template(self):
        hancock = factories.Pirate(name='Boa Hancock', bounty=None, crew=None)
        marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=None)
        response = self.client.get(reverse('bounties:index'), data={'pirate-search-field':'Boa'})
        list_context = response.context['pirates']
        correct_results = Pirate.objects.filter(name__icontains='Boa')

        self.assertIn(hancock, list_context)
        self.assertIn(marigold, list_context)
        self.assertEqual(correct_results.count(), list_context.count())
