import unittest
import sys

sys.path.insert(0, '../')
from src import data


class TestEmbedding(unittest.TestCase):

    def setUp(self):

        self.en_fr_test_file = "../Data/wikiclir2018/data_en_fr/test1.txt"
        
        for loaded_data in data.get_data(self.en_fr_test_file, 10):
            print(loaded_data.relevance)
            print(loaded_data.query)
            print(loaded_data.doc)

    def tearDown(self):
        pass

    def test_dummy(self):
        self.assertEqual(1, 1)


if __name__=="__main__":
    unittest.main()
