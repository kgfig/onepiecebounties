from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class HomePageTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_search_for_a_pirate_and_see_his_bounty(self):
        # The marines have put up an online billboard for pirate bounties.
        # Coby hears about this and goes to check it out.
        self.browser.get('http://localhost:8000/onepiecebounties/')

        # He notices the title read "WANTED | Unofficial list of bounties in One Piece"
        self.assertEqual('WANTED | Unofficial list of bounties in One Piece', self.browser.title)
        
        # and huge header read "WANTED" on the home page.
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual('WANTED', header_text)
                  
        # Near the top of the page just below the header are a search field
        # which invites him to search for a pirate
        inputbox = self.browser.find_element_by_tag_name('input')
        self.assertEqual('search-field', inputbox.id)
        self.assertEqual(
            'Search for a pirate', inputbox.get_attribute('placeholder')
        )

        # He remembers his old friend and types "Luffy" in the search field.
        inputbox.send_keys('Luffy')

        # As he was typing, the name "Monkey D. Luffy" shows up as the only suggestion in the list.
        time.sleep(3)
        suggestions = self.browser.find_elements_by_tag_name('option')
        name_found = [True for suggested_name in suggestions if pirate_name == 'Monkey D. Luffy' ]
        self.assertEqual(True, name_found)

        # He presses down and hits Enter to select "Monkey D. Luffy".
        inputbox.send_keys(Keys.DOWN)
        inputbox.send_keys(Keys.ENTER)
        
        # The search field now reads "Monkey D. Luffy".
        inputbox = self.browser.find_element_by_tag_name('input')
        self.assertEqual('Monkey D. Luffy', inputbox.get_attribute('value'))

        # Beside the field is a "Search" button, he clicks on it.
        self.find_element_by_id('search').click()
        
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

if __name__ == '__main__':
    unittest.main(warnings='ignore')
