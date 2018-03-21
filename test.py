import unittest
import webscraper

class Webscraper(unittest.TestCase):
    def test_scraping(self):
        with open('thumbscraper_input.json') as f:
            webscraper.scrape_text(f.read())


if __name__ == '__main__':
    unittest.main()
