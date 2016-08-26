from django.core.urlresolvers import resolve
from django.test import TestCase
from .views import index
from .models import Pirate

class HomePageTest(TestCase):

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

