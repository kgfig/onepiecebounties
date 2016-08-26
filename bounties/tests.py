from django.core.urlresolvers import resolve
from django.test import TestCase
from .views import index

class HomePageTest(TestCase):

    def test_can_resolve_to_home_page_view(self):
        found = resolve('/onepiecebounties/')
        self.assertEqual(found.func, index)
