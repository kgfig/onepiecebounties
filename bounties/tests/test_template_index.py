from django.conf import settings
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.template.defaultfilters import slugify
from bounties import factories, views
from bounties.models import Crew, Pirate

class IndexTemplateTest(TestCase):

    def test_template_returns_home_template(self):
        response = self.client.get(reverse('bounties:index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_template_has_all_pirate_names_in_suggestions(self):
        luffy = factories.Pirate()
        alvida = factories.Pirate(name='Iron Mace Alvida', bounty=None, crew=None)
        shanks = factories.Pirate(name='Red-Haired Shanks', bounty=None, crew=None)
        response = self.client.get(reverse('bounties:index'))
        self.assertContains(response, '<option value="%s">%s</option>' % (luffy.name, luffy.name,), html=True)
        self.assertContains(response, '<option value="%s">%s</option>' % (alvida.name, alvida.name,), html=True)
        self.assertContains(response, '<option value="%s">%s</option>' % (shanks.name, shanks.name,), html=True)

