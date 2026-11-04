import unittest
from zero_naz import scan, normalize

def ids(text, ambiguous=False):
    return {hit['id'] for hit in scan(text,ambiguous)}

class MatcherTests(unittest.TestCase):
    def test_strong_signal(self):
        self.assertIn('rahowa',ids('RAHOWA'))

    def test_benign_numbers_default(self):
        for text in ['I am 18.', 'Call 311 for municipal services.', 'Call 110.', 'The price is 1488 dollars.']:
            self.assertEqual(ids(text),set())

    def test_boundaries(self):
        for text in ['classical', 'assignment', 'ahoy', '3110', '14880', 'x1488x']:
            self.assertEqual(ids(text,True),set())
        self.assertIn('1488',ids('user_1488',True))

    def test_normalization(self):
        self.assertIn('rahowa',ids('ＲＡＨＯＷＡ'))
        self.assertIn('rahowa',ids('RA\u200bHOWA'))
        self.assertIn('de-9',ids('MEINE   EHRE HEISST TREUE'))
        self.assertEqual(normalize('Straße'),'strasse')

    def test_echo(self):
        self.assertIn('echo',ids('(((Example Person)))',True))
        self.assertIn('echo',ids('((((Example Person))))',True))
        self.assertNotIn('echo',ids('(normal parentheses)',True))

    def test_historical_quote_still_requires_review(self):
        hits=scan('The museum explains the term Holohoax.')
        self.assertTrue(hits)
        self.assertTrue(all(h['action']=='human_review' for h in hits))

    def test_emoji_not_invented(self):
        self.assertEqual(ids('☀️ 🐸 👌 ⚡ 💀',True),set())

    def test_runes_ambiguous(self):
        self.assertEqual(ids('ᛟ'),set())
        self.assertIn('othala',ids('ᛟ',True))

if __name__=='__main__':
    unittest.main()
