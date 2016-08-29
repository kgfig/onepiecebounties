from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bounties import factories

class HomePageTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        strawhat = factories.Crew()
        alvida_crew = factories.Crew(name='Alvida Pirates')
        factories.Pirate(crew=strawhat)
        factories.Pirate(name='Iron Mace Alvida', crew=alvida_crew)
        factories.Pirate(name='God Usopp', bounty=200000000, crew=strawhat)
        factories.Pirate(name='Tony Tony Chopper', bounty=100, crew=strawhat)
        factories.Pirate(name='Roronoa Zoro', bounty=320000000, crew=strawhat)
        factories.Pirate(name='Sanji', bounty=177000000, crew=strawhat)
        factories.Pirate(name='Nico Robin', bounty=130000000, crew=strawhat)
        factories.Pirate(name='Cyborg Franky', bounty=94000000, crew=strawhat)
        factories.Pirate(name='Nami', bounty=66000000, crew=strawhat)
        factories.Pirate(name='Soul King', bounty=83000000, crew=strawhat)

    def tearDown(self):
        self.browser.quit()

    def _check_header_text(self, header, expected_header_text='WANTED'):
        self.assertEqual(expected_header_text, header.text)

    def _check_search_field_attributes(self, inputbox, input_type='search', placeholder_text='Search for a pirate', input_name='pirate-search-field', input_list='pirate-names'):
        self.assertEqual(input_type, inputbox.get_attribute('type'))
        self.assertEqual(placeholder_text, inputbox.get_attribute('placeholder'))
        self.assertEqual(input_name, inputbox.get_attribute('name'))
        self.assertEqual(input_list, inputbox.get_attribute('list'))

    def _check_datalist_exists(self, datalist, datalist_options):
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
        home_suggestions = self.browser.find_elements_by_tag_name('option')
        self._check_datalist_exists(home_datalist, home_suggestions)
        self.assertIn('Iron Mace Alvida', [pirate.get_attribute('value') for pirate in home_suggestions])

        # He stops before he could finish the search.
        # He remembers his old friend who freed him and inspired him to pursue his dream of becoming a marine.
        # He clears the search field and types "Luffy" instead.
        inputbox.clear()
        inputbox.send_keys('Luffy')

        # As he was typing, the name "Monkey D. Luffy" shows up as the only suggestion in the list.
        time.sleep(3)
        self.assertIn('Monkey D. Luffy', [pirate.get_attribute('value') for pirate in home_suggestions])

        # He presses down and hits Enter to select "Monkey D. Luffy".
        inputbox.send_keys(Keys.DOWN)
        inputbox.send_keys(Keys.ENTER)
        
        # The search field now reads "Monkey D. Luffy".
        inputbox = self.browser.find_element_by_tag_name('input')
        self.assertEqual('Monkey D. Luffy', inputbox.get_attribute('value'))

        # Beside the field is a "Search" button, he clicks on it.
        self.browser.find_element_by_id('search-button').click()
        
        # The page changes.
        self.assertRegex(self.browser.current_url, '/onepiecebounties/\d+/')

        # He sees the name, bounty, the crew name and photo of his friend on the page.
        luffy_name = self.browser.find_element_by_class_name('name').text
        self.assertEqual('Monkey D. Luffy', luffy_name)

        luffy_bounty = self.browser.find_element_by_class_name('bounty').text
        self.assertEqual('500,000,000', luffy_bounty)
        
        luffy_crew = self.browser.find_element_by_class_name('crew').text
        self.assertEqual('Straw Hat Crew', luffy_crew)

        luffy_image = self.browser.find_element_by_tag_name('img')
        image_src = luffy_image.get_attribute('src')
        self.assertTrue('monkey-d-luffy' in image_src)

        # He realizes how far his friend has come since that heartbreaking incident at Marineford.
        # He was glad to see him again in high spirits with a crew that he can always count on.
        
        # He notices that the huge title "WANTED" is still on top of the page.
        profile_header = self.browser.find_element_by_tag_name('h1')
        self._check_header_text(profile_header)

        # Near the top-right corner of the page are a search field and a button.
        profile_inputbox = self.browser.find_element_by_tag_name('input')
        self._check_search_field_attributes(profile_inputbox)
        profile_search_button = self.browser.find_element_by_id('search-button');
        self.assertEqual(profile_search_button.get_attribute('value'), 'Search')

        profile_datalist = self.browser.find_element_by_tag_name('datalist')
        profile_options = self.browser.find_elements_by_tag_name('option')
        self._check_datalist_exists(profile_datalist, profile_options)

        # He decides to search for Luffy' crewmates and types "Straw Hat" in the search field.
        profile_inputbox.send_keys('Straw Hat')

        # The page updates.
        self.assertRegex(self.browser.current_url, '/onepiecebounties/')

        # He sees the links to the names of each Straw Hat Crew member.
        self.fail('Continue this some other time')        
