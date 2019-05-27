import unittest
import sys

sys.path.insert(0, '../')
from src import data


class TestData(unittest.TestCase):

    def setUp(self):

        self.en_fr_test_file = "../Data/wikiclir2018/data_en_fr/test1.txt"
        
        for loaded_data in data.get_data(self.en_fr_test_file, 10):
            print(loaded_data.relevance)
            print(loaded_data.query)
            print(loaded_data.doc)

        self.english_processor = data.TextProcessor("english")


    def tearDown(self):
        pass


    def test_clean(self):
        
        dirty_str = "This is a sent"
        self.assertEqual(self.english_processor.clean(dirty_str), "this is a sent")

        dirty_str = ""
        self.assertEqual(self.english_processor.clean(dirty_str), "")

        dirty_str = "This is a sent \n"
        self.assertEqual(self.english_processor.clean(dirty_str), "this is a sent")

        dirty_str = "   This is a sent \r  "
        self.assertEqual(self.english_processor.clean(dirty_str), "this is a sent")

        dirty_str = "   This is a, sent ,\n"
        self.assertEqual(self.english_processor.clean(dirty_str), "this is a sent")

        dirty_str = "   This is a, \t sent ,\n"
        self.assertEqual(self.english_processor.clean(dirty_str), "this is a   sent")
        
        dirty_str = "   This is a,; sent ,\n"
        self.assertEqual(self.english_processor.clean(dirty_str), "this is a sent")

        dirty_str = "   This is a sent.\nThis is another sent."
        self.assertEqual(self.english_processor.clean(dirty_str), "this is a sent this is another sent")

    def test_tokenize(self):

        in_str = "this is a sent"
        self.assertEqual(self.english_processor.tokenize(in_str), ["sent"])

        in_str = "word1          word2"
        self.assertEqual(self.english_processor.tokenize(in_str), ["word1", "word2"])

if __name__=="__main__":
    unittest.main()
