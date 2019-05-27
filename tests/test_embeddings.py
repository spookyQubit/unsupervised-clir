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
        
        target_embeddings = source_embeddings  # testing scenario where src = trg
        target_id2word = source_id2word # testing scenario where src = trg

        knn_trg_ids, knn_scores_of_trg_ids = embeddings.get_knn(src_word=source_word, 
                                                                src_emb=source_embeddings, 
                                                                src_id2word=source_id2word, 
                                                                trg_emb=target_embeddings, 
                                                                trg_id2word=target_id2word, 
                                                                K=5)

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
        
        source_embeddings = self.english_emb.embeddings
        source_id2word = self.english_emb.id2word
        
        target_embeddings = self.french_emb.embeddings 
        target_id2word = self.french_emb.id2word

        knn_trg_ids, knn_scores_of_trg_ids = embeddings.get_knn(src_word=source_word, 
                                                                src_emb=source_embeddings, 
                                                                src_id2word=source_id2word, 
                                                                trg_emb=target_embeddings, 
                                                                trg_id2word=target_id2word, 
                                                                K=5)

        knn_target_words = [target_id2word[idx] for idx in target_id2word]
        self.assertIn(expected_target_word, knn_target_words)


if __name__=="__main__":
    unittest.main()
