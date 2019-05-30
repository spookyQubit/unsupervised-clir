import unittest
import sys
import numpy as np

sys.path.insert(0, '../')
from src import embeddings


class TestEmbedding(unittest.TestCase):

    def setUp(self):

        self.en_embeddings_file = "../Embeddings/Conneau/wiki.multi.en.vec"
        self.fr_embeddings_file = "../Embeddings/Conneau/wiki.multi.fr.vec"

        self.english_emb = embeddings.Embeddings(self.en_embeddings_file, "english")
        self.french_emb = embeddings.Embeddings(self.fr_embeddings_file, "french")

        self.wordTranslator = embeddings.WordTranslator(self.english_emb, self.french_emb, 5)

    def tearDown(self):
        pass

    def test_canneau_supervised_english_french_dimension_match(self):
        '''
        Assert that the embedding dimensions of the various languages are same. 
        '''
        print("In test_canneau_supervised_english_french_dimension_match")
        self.assertEqual(self.english_emb.dim, self.french_emb.dim)
    
    def test_canneau_supervised_knn_with_same_trg_and_src_languages(self): 
        '''
        If the source and target languages are the same, make sure that the 
        function get_knn returns the id of word in target language which is the 
        same as the source word.  
        '''

        print("In test_canneau_supervised_knn_with_same_trg_and_src_languages")

        source_word = "cat"

        source_embeddings = self.english_emb.embeddings
        source_id2word = self.english_emb.id2word
        source_word2id = self.english_emb.word2id
        
        target_embeddings = source_embeddings  # testing scenario where src = trg
        target_id2word = source_id2word # testing scenario where src = trg

        wTranslator = embeddings.WordTranslator(self.english_emb, self.english_emb, 5)


        knn_trg_ids, knn_scores_of_trg_ids = wTranslator.get_knn(source_word)
        self.assertEqual(source_word, target_id2word[knn_trg_ids[0]])

    def test_canneau_supervised_knn_with_diff_trg_and_src_languages(self):
        '''
        For a given word in source language, say "cat" in english, assert that the 
        words in target language returned by get_knn contains the translation of source 
        word, "chat" in french in this case. 
        '''

        print("In test_canneau_supervised_knn_with_same_trg_and_src_languages")

        source_word = "cat"
        expected_target_word = "chat"

        knn_trg_ids, knn_scores_of_trg_ids = self.wordTranslator.get_knn(source_word)
        
        knn_target_words = [self.french_emb.id2word[idx] for idx in knn_trg_ids]
        print(knn_target_words)
        self.assertIn(expected_target_word, knn_target_words)


if __name__=="__main__":
    unittest.main()
