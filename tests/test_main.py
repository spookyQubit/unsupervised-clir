import unittest
import sys

sys.path.insert(0, '../')
from src import main


class TestMain(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_input_and_output_data_file_names(self):
        wiki_dir='../DataDir' 
        query_wiki_lang='qLang' 
        doc_wiki_lang='dLang'
        f_name='dev'

        in_path, out_path = main.get_input_and_output_data_file_names(wiki_dir, 
                                                                      query_wiki_lang, 
                                                                      doc_wiki_lang, 
                                                                      f_name)
        self.assertEqual(in_path, '../DataDir/data_qLang_dLang/dev.txt')
        self.assertEqual(out_path, '../DataDir/data_qLang_dLang/dev_processed.txt')


if __name__ == "__main__":
    unittest.main()

