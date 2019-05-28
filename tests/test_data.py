import unittest
import sys
import os
from collections import Counter

sys.path.insert(0, '../')
from src import data


class TestTextProcessor(unittest.TestCase):

    def setUp(self):

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
        self.assertEqual(self.english_processor.clean(dirty_str), "this is a  sent")

        dirty_str = "   This is a, \t sent ,\n"
        self.assertEqual(self.english_processor.clean(dirty_str), "this is a    sent")
        
        dirty_str = "   This is a,; sent ,\n"
        self.assertEqual(self.english_processor.clean(dirty_str), "this is a   sent")

        dirty_str = "   This is a sent.\nThis is another sent."
        self.assertEqual(self.english_processor.clean(dirty_str), "this is a sent  this is another sent")

    def test_tokenize(self):

        in_str = "this is a sent"
        self.assertEqual(self.english_processor.tokenize(in_str), ["sent"])

        in_str = "word1          word2"
        self.assertEqual(self.english_processor.tokenize(in_str), ["word1", "word2"])

    def test_invalid_lang_for_class_TextProcessor(self):

        with self.assertRaises(ValueError) as context:

            some_bad_lang = "engxyz"
            invalid_processor = data.TextProcessor(some_bad_lang)

        self.assertTrue('Do not support for language={} to get stopwords'.format(some_bad_lang) in str(context.exception))




class TestGetData(unittest.TestCase):
    def setUp(self):
        self.temp_file = './temp_data.txt'

    def tearDown(self):
       os.remove(self.temp_file) 

    def test_get_data_all_entries_correct_1(self):

        print("in testgetdata")
        
        with open(self.temp_file, 'w') as f:
            f.write("1\tthis is a query\tthis is a doc")

        for loaded_data in data.get_data(self.temp_file, 1):
            print(loaded_data.query)
            self.assertEqual(loaded_data.relevance, 1)
            self.assertEqual(loaded_data.query, "this is a query")
            self.assertEqual(loaded_data.doc, "this is a doc")
            self.assertEqual(loaded_data.doc_idx, 0)
    
    def test_get_data_all_entries_correct_2(self):
        
        with open(self.temp_file, 'w') as f:
            f.write("1\tthis is a query 2\tthis is a doc 2")

        for loaded_data in data.get_data(self.temp_file, 1):
            self.assertEqual(loaded_data.relevance, 1)
            self.assertEqual(loaded_data.query, "this is a query 2")
            self.assertEqual(loaded_data.doc, "this is a doc 2")
            self.assertEqual(loaded_data.doc_idx, 0)

    def test_get_data_all_relevance_incorrect(self):
        with open(self.temp_file, 'w') as f:
            f.write("wrong_relevance\tthis is a query\tthis is a doc")

        for loaded_data in data.get_data(self.temp_file, 1):
            self.assertEqual(loaded_data.relevance, -1)
            self.assertEqual(loaded_data.query, "")
            self.assertEqual(loaded_data.doc, "")
            self.assertEqual(loaded_data.doc_idx, 0)

    def test_get_data_all_correct_and_incorrect(self):
        with open(self.temp_file, 'w') as f:
            f.write("1\tthis is a query\tthis is a doc\n")
            f.write("wrong_relevance\tthis is a query\tthis is a doc\n")
            f.write("2\tthis is a query 2\tthis is a doc 2\n")

        for loaded_data in data.get_data(self.temp_file, 2):
            if loaded_data.doc_idx == 0:
                self.assertEqual(loaded_data.relevance, 1)
                self.assertEqual(loaded_data.query, "this is a query")
                self.assertEqual(loaded_data.doc, "this is a doc\n")
                self.assertEqual(loaded_data.doc_idx, 0)

            elif loaded_data.doc_idx == 1:
                self.assertEqual(loaded_data.relevance, -1)
                self.assertEqual(loaded_data.query, "")
                self.assertEqual(loaded_data.doc, "")
                self.assertEqual(loaded_data.doc_idx, 1)

            elif loaded_data.doc_idx == 2:
                self.assertEqual(loaded_data.relevance, 2)
                self.assertEqual(loaded_data.query, "this is a query 2")
                self.assertEqual(loaded_data.doc, "this is a doc 2\n")
                self.assertEqual(loaded_data.doc_idx, 2)



if __name__=="__main__":
    unittest.main()
