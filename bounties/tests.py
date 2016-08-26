from django.core.urlresolvers import resolve
from django.test import TestCase
from .views import index

class HomePageTest(TestCase):

    def test_can_resolve_to_home_page_view(self):
        found = resolve('/onepiecebounties/')
        self.assertEqual(found.func, index)

    def test_returns_home_template(self):
        response = self.client.get('/onepiecebounties/')
        self.assertTemplateUsed(response, 'index.html')

    def test_returns_OK(self):
        response = self.client.get('/onepiecebounties/')
        self.assertEqual(response.status_code, 200)

    def test_suggests_name_in_search_field(self):
        response = self.client.get('/onepiecebounties/')
        self.assertContains(response, '<option value="Iron Mace Alvida">Iron Mace Alvida</option>')
