import unittest

from scripts import extractkeywords 

class TestExtractKeywords(unittest.TestCase):
    def test_non_english(self):
        keywords = extractkeywords.extract_keywords("আপনি কেমন আছেন");
        self.assertEqual(keywords,"")
    
    def test_english(self):
        keywords = extractkeywords.extract_keywords("not-for-profit organization");
        self.assertEqual(keywords,"profit organization")

if __name__=='__main__':
	unittest.main()