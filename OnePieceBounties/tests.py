from django.core.urlresolvers import resolve
from django.test import TestCase

class HomePageTest(self):

    def test_can_resolve_to_home_page_view(self):
        found = resolve('/onepiecebounties/')
        self.assertEqual(True, found)
