from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class HomePageTest(LiveServerTestCase):
    fixtures = ['pirates.yaml']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_search_for_a_pirate_and_see_his_bounty(self):
        # The marines have put up an online billboard for pirate bounties.
        # Coby hears about this and goes to check it out.
        self.browser.get(self.live_server_url + '/onepiecebounties/')

        # He notices the title read "WANTED | Unofficial list of bounties in One Piece"
        self.assertEqual('WANTED | Unofficial list of bounties in One Piece', self.browser.title)
        
        # and huge header read "WANTED" on the home page.
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual('WANTED', header_text)
                  
        # Near the top of the page just below the header are a search field
        # which invites him to search for a pirate
        inputbox = self.browser.find_element_by_tag_name('input')
        self.assertEqual('search', inputbox.get_attribute('type'))
        self.assertEqual('Search for a pirate', inputbox.get_attribute('placeholder'))
        self.assertEqual('pirate-search-field', inputbox.get_attribute('name'))
        self.assertEqual('pirate-names', inputbox.get_attribute('list'))

        # His past quickly flashes back.
        # He types the name of his former captain from when he was still a pirate.
        inputbox.send_keys('Alvida')

        # As he was typing, the name "Iron Mace Alvida" shows up in the suggestions.
        time.sleep(3)
        suggestion_list = self.browser.find_element_by_tag_name('datalist')
        self.assertEqual('pirate-names', suggestion_list.get_attribute('id'))
        self.assertIsNotNone(suggestion_list, 'No datalist found for input')
        suggestion_options = self.browser.find_element_by_tag_name('option')
        self.assertIsNotNone(suggestion_options, 'No options for datalist element')
        
        suggestions = self.browser.find_elements_by_tag_name('option')
        self.assertIsNotNone(suggestions)
        self.assertIn('Iron Mace Alvida', [pirate.get_attribute('value') for pirate in suggestions])

        # He stops before he could finish the search.
        # He remembers his old friend who freed him and inspired him to pursue his dream of becoming a marine.
        # He clears the search field and types "Luffy" instead.
        inputbox.clear()
        inputbox.send_keys('Luffy')

        # As he was typing, the name "Monkey D. Luffy" shows up as the only suggestion in the list.
        time.sleep(3)
        suggestions = self.browser.find_elements_by_tag_name('option')
        self.assertIn('Monkey D. Luffy', [pirate.get_attribute('value') for pirate in suggestions])

        # He presses down and hits Enter to select "Monkey D. Luffy".
        inputbox.send_keys(Keys.DOWN)
        inputbox.send_keys(Keys.ENTER)
        
        # The search field now reads "Monkey D. Luffy".
        inputbox = self.browser.find_element_by_tag_name('input')
        self.assertEqual('Monkey D. Luffy', inputbox.get_attribute('value'))

        # Beside the field is a "Search" button, he clicks on it.
        self.browser.find_element_by_id('search-button').click()
        
        # The page changes.
        self.assertRegex('/onepiecebounties/(\w+)/', self.browser.current_url)

        # He sees the name, photo and bounty of ONLY his friend on the page.
        luffy_name = self.browser.find_element_by_class_name('name').text
        self.assertEqual('Monkey D. Luffy', luffy_name)

        luffy_crew = self.browser.find_element_by_class_name('crew').text
        self.assertEqual('Straw Hat Crew', luffy_crew)

        luffy_bounty = self.browser.find_element_by_class_name('bounty').text
        self.assertEqual('500,000,000', luffy_bounty)
        
        # He realizes how far they've come in their chosen paths.
        # He leaves his computer to return to his post.
