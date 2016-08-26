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

    def test_view_passes_correct_context_to_template(self):
        pirates = [{'name': 'Iron Mace Alvida'},
                   {'name': 'Monkey D. Luffy'},
                   ]
        response = self.client.get('/onepiecebounties/')
        self.assertEqual(response.context['pirates'], pirates)
        
    def test_display_correct_names_in_suggestions(self):
        pirates = [{'name': 'Iron Mace Alvida'},
                   {'name': 'Monkey D. Luffy'},
                   ]
        response = self.client.get('/onepiecebounties/')
        
        self.assertContains(response, pirates[0]['name'])
        self.assertContains(response, pirates[1]['name'])
        self.assertNotContains(response, "{'name':")
