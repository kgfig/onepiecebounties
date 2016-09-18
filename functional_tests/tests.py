from bounties import factories
from bounties.models import Pirate
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

SEARCH_PLACEHOLDER = 'Search for a pirate...'
SEARCH_INPUT_TYPE = 'search'
SEARCH_INPUT_NAME = 'pirate-search-field'
SEARCH_DATALIST_ID = 'pirate-names'
HEADER_TEXT = 'WANTED'

class BountiesTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        strawhat = factories.Crew()
        alvida_crew = factories.Crew(name='Alvida Pirates')
        kuja = factories.Crew(name='Kuja Pirates')
        self.luffy = factories.Pirate(crew=strawhat)
        self.alvida = factories.Pirate(name='Iron Mace Alvida', crew=alvida_crew)
        factories.Pirate(name='God Usopp', bounty=200000000, crew=strawhat)
        factories.Pirate(name='Chopper', bounty=100, crew=strawhat)
        factories.Pirate(name='Roronoa Zoro', bounty=320000000, crew=strawhat)
        factories.Pirate(name='Sanji', bounty=177000000, crew=strawhat, wanted_status=Pirate.ONLY_ALIVE)
        factories.Pirate(name='Nico Robin', bounty=130000000, crew=strawhat)
        factories.Pirate(name='Franky', bounty=94000000, crew=strawhat)
        factories.Pirate(name='Nami', bounty=66000000, crew=strawhat)
        factories.Pirate(name='Soul King', bounty=83000000, crew=strawhat)
        self.hancock = factories.Pirate(name='Boa Hancock', bounty=None, crew=kuja, wanted_status=None)
        self.sandersonia = factories.Pirate(name='Boa Sandersonia', bounty=None, crew=kuja, wanted_status=None)
        self.marigold = factories.Pirate(name='Boa Marigold', bounty=None, crew=kuja, wanted_status=None)

    def tearDown(self):
        self.browser.quit()

    def _check_header_text(self, header, expected_header_text=HEADER_TEXT):
        self.assertEqual(expected_header_text, header.text)

    def _check_search_field_attributes(self, inputbox, input_type=SEARCH_INPUT_TYPE, placeholder_text=SEARCH_PLACEHOLDER, input_name=SEARCH_INPUT_NAME, input_list=SEARCH_DATALIST_ID):
        self.assertEqual(input_type, inputbox.get_attribute('type'))
        self.assertEqual(placeholder_text, inputbox.get_attribute('placeholder'))
        self.assertEqual(input_name, inputbox.get_attribute('name'))
        self.assertEqual(input_list, inputbox.get_attribute('list'))

    def _check_autocomplete_options(self, options, pirate):
        self.assertIn(pirate.name, [option.get_attribute('value') for option in options])

    def _check_pirate_data_in_profile_page_elements(self, pirate):
        name_element = self.browser.find_element_by_class_name('name')
        self.assertEqual(pirate.name.upper(), name_element.text.upper())

        self._check_search_result_bounty_class(pirate)
        self._check_wanted_status(pirate)

        image_element = self.browser.find_element_by_tag_name('img')
        image_src = image_element.get_attribute('src')
        self.assertTrue(pirate.filename() in image_src)

    def _check_wanted_status(self, pirate):
        if pirate.wanted_status:
            status_elements = self.browser.find_elements_by_class_name('wanted-status')
            self.assertIn(pirate.get_wanted_status_display().upper(), [element.text.upper() for element in status_elements])
        else:
            pass

    """
    Returns the first matching <a> tag if the url it points to contains the link to the pirate's profile.
    Returns None otherwise.
    """
    def _find_link_to_profile(self, pirate):
        pirate_url = '/onepiecebounties/%d/' % (pirate.id,)
        name_links = self.browser.find_elements_by_tag_name('a')
        matching_urls = [link_element for link_element in name_links if pirate_url in link_element.get_attribute('href')]
        return matching_urls[0] if len(matching_urls) > 0 else None

    """
    Asserts True if a matching <a> is found for this pirate
    """
    def _check_search_result_name_links(self, pirate):
        pirate_link = self._find_link_to_profile(pirate)
        name_links = self.browser.find_elements_by_tag_name('a')
        self.assertIsNotNone(pirate_link, 'No links found for pirate with id=%d' % (pirate.id,))
        
    def _check_search_result_bounty_class(self, pirate):
        if pirate.bounty:
            bounty_elements = self.browser.find_elements_by_class_name('bounty')
            self.assertIn('{:,}'.format(pirate.bounty), [element.text for element in bounty_elements])

    def _check_search_result_crew_class(self, pirate):
        crew_elements = self.browser.find_elements_by_class_name('crew')
        self.assertIn(pirate.crew.name.upper(), [element.text.upper() for element in crew_elements])

    # TODO improve code in asserting that the filename can be matched
    # (using regex) in one of the image elements' src attribute
    def _check_search_result_image_tags(self, pirate):
        image_elements = self.browser.find_elements_by_tag_name('img')
        matched = False
        pattern = '.*/static/images/pirates/' + pirate.filename()
        exp = re.compile(pattern)

        for image in image_elements:
            if exp.match(image.get_attribute('src')):
                matched = True
                break
            
        self.assertTrue(matched, 'Pirate filename %s not found in %s' % (pattern, image.get_attribute('src'),))

    def _check_list_in_search_results(self, pirates):
        len_pirates = len(pirates)
        name_elements = self.browser.find_elements_by_class_name('name')
        self.assertEqual(len(name_elements), len_pirates)

        pirates_with_bounty = [ some_pirate for some_pirate in pirates if some_pirate.bounty ]
        bounty_elements = self.browser.find_elements_by_class_name('bounty') 
        self.assertEqual(len(bounty_elements), len(pirates_with_bounty))

        pirates_with_crew = [ some_pirate for some_pirate in pirates if some_pirate.crew ]
        crew_elements = self.browser.find_elements_by_class_name('crew')
        self.assertEqual(len(crew_elements), len(pirates_with_crew))

        poster_elements = self.browser.find_elements_by_class_name('poster')
        self.assertEqual(len(poster_elements), len_pirates)

        for pirate in pirates:
            self._check_search_result_name_links(pirate)
            self._check_search_result_crew_class(pirate)
            self._check_wanted_status(pirate)
            self._check_search_result_image_tags(pirate)

    def _check_datalist_exists(self, datalist=None, datalist_options=None):
        datalist = datalist if datalist else self.browser.find_element_by_tag_name('datalist')
        datalist_options = datalist_options if datalist_options else self.browser.find_elements_by_tag_name('option')
        self.assertEqual('pirate-names', datalist.get_attribute('id'))
        self.assertIsNotNone(datalist, 'No datalist found for input')
        self.assertIsNotNone(datalist_options, 'No options for datalist element')

    def test_can_search_for_a_pirate_and_see_his_bounty(self):
        # The marines have put up an online billboard for pirate bounties.
        # Coby hears about this and goes to check it out.
        self.browser.get(self.live_server_url + '/onepiecebounties/')

        # He notices the title read "WANTED | Unofficial list of bounties in One Piece"
        self.assertEqual('WANTED | Unofficial list of bounties in One Piece', self.browser.title)
        
        # and huge header read "WANTED" on the home page.
        header = self.browser.find_element_by_tag_name('h1')
        self._check_header_text(header)
                  
        # Near the top of the page just below the header is a search field
        # which invites him to search for a pirate.
        inputbox = self.browser.find_element_by_tag_name('input')
        self._check_search_field_attributes(inputbox)

        # His past quickly flashes back.
        # He types the name of his former captain from when he was still a pirate.
        inputbox.send_keys('Alvida')

        # As he was typing, the name "Iron Mace Alvida" shows up in the suggestions.
        time.sleep(3)
        home_datalist = self.browser.find_element_by_tag_name('datalist')
        home_options = self.browser.find_elements_by_tag_name('option')
        self._check_datalist_exists(home_datalist, home_options)
        self._check_autocomplete_options(home_options, self.alvida)

        # He stops before he could finish the search.
        # He remembers his old friend who freed him and inspired him to pursue his dream of becoming a marine.
        # He clears the search field and types "Luffy" instead.
        inputbox.clear()
        inputbox.send_keys('Luffy')

        # As he was typing, the name "Monkey D. Luffy" shows up as the only suggestion in the list.
        time.sleep(3)
        self._check_autocomplete_options(home_options, self.luffy)

        # He presses down and hits Enter to select "Monkey D. Luffy".
        inputbox.send_keys(Keys.DOWN)
        inputbox.send_keys(Keys.ENTER)
        
        # The search field now reads "Monkey D. Luffy".
        inputbox = self.browser.find_element_by_tag_name('input')
        self.assertEqual(self.luffy.name, inputbox.get_attribute('value'))

        # Again, he hits Enter. The page changes.
        inputbox.send_keys(Keys.ENTER)
        self.assertRegex(self.browser.current_url, '/onepiecebounties/\d+/')

        # He sees the name, bounty, the crew name and photo of his friend on the page.
        self._check_pirate_data_in_profile_page_elements(self.luffy)

        # He notices that the huge title "WANTED" is still on top of the page.
        profile_header = self.browser.find_element_by_tag_name('h1')
        self._check_header_text(profile_header)

        # Near the top-right corner of the page is a search field.
        profile_inputbox = self.browser.find_element_by_tag_name('input')
        self._check_search_field_attributes(profile_inputbox)
        
        profile_datalist = self.browser.find_element_by_tag_name('datalist')
        profile_options = self.browser.find_elements_by_tag_name('option')
        self._check_datalist_exists()

        # Rumors say that since that fateful day at Marineford,
        # Luffy spent the next 2 years in the island of women under Boa Hancock's protection.
        # His curiosity is piqued. He types "Boa" in the search field.
        profile_inputbox.send_keys('Boa')

        # TODO/NOTE: Should this be tested? How?
        # See the pirates in the suggestions.
        time.sleep(3)
        self._check_autocomplete_options(profile_options, self.hancock)
        self._check_autocomplete_options(profile_options, self.sandersonia)
        self._check_autocomplete_options(profile_options, self.marigold)
        
        # He presses enter.
        profile_inputbox.send_keys(Keys.ENTER)

        # The page updates.
        self.assertRegex(self.browser.current_url, '/onepiecebounties/')

        # The page shows the crew name, photos and names of the 3 Boa sisters.
        # He notices that the names are actually links.
        self._check_list_in_search_results([self.hancock, self.sandersonia, self.marigold])

        # He clicks on Boa Hancock's name.
        boa_link = self._find_link_to_profile(self.hancock)
        boa_link.click()

        # The page updates.
        new_profile_url = '/onepiecebounties/%d/' % (self.hancock.id,)
        self.assertRegex(self.browser.current_url, new_profile_url)

        # He sees her information on the page.
        self._check_pirate_data_in_profile_page_elements(self.hancock)

        # Curiosity now satisfied, Coby leaves the computer and goes to sleep.
        
        ## Intro for a user story that will be pushed down to the bottom of the priority list:
        ## He realizes how far his friend has come since that heartbreaking incident at Marineford.
        ## He is glad to see him again in high spirits with a crew that he can always count on.
        ## He decides to search for his crewmates and types "Straw Hat" in the search field.
        
