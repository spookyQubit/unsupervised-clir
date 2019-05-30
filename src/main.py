import sys
from os import path
import pickle
from collections import Counter
import numpy as np

import data
import embeddings


# Data
g_wikiclir2018_dir = "../Data/wikiclir2018"
g_query_wikiclir2018_language = "en"
g_doc_wikiclir2018_language = "fr"

# required for stopwords
g_wikiclir2018_language_to_nltk_language = {"en": "english", 
                                            "fr": "french", 
                                            "ja": "japanese"}  
g_data_mode = 'dev'
g_data_mode_to_f_name = {'dev': 'dev', 'test': 'test1', 'train': 'train'}

# Embeddings
g_query_embeddings_file = "../Embeddings/Conneau/wiki.multi.en.vec"
g_doc_embeddings_file = "../Embeddings/Conneau/wiki.multi.fr.vec"
g_KNN_K = 5

g_max_samples = 10000
g_use_best_translation_only = True  # only True supported for now
g_mu = 1000

def get_input_and_output_data_file_names(wiki_dir, 
                                         query_wiki_lang, 
                                         doc_wiki_lang, 
                                         f_name):
    '''
    param wiki_dir: Relative path to where wikiclir2018 data is stored
    param query_wiki_lang: Query language. Assumed to be compatible with 
                           lang in stopwords.words(lang)
    param doc_wiki_lang: Doc language. Assumed to be compatible with 
                         lang in stopwords.words(lang)
    param f_name: train or dev or test1 depending upon the data_mode
    returns: in_file_path is the file from which to read data
             out_individual_file_path is the file to store processed data for per docment
             out_all_file_path is the file to store processed data for all doucuments 
    '''

    data_dir = '_'.join(['data', query_wiki_lang, doc_wiki_lang])

    in_f_name = f_name + '.txt'
    out_individual_f_name = f_name + '_individual_processed' + '.txt'
    out_all_f_name = f_name + '_all_processed' + '.txt'
    
    in_file_path = path.join(wiki_dir, data_dir, in_f_name)
    out_individual_file_path = path.join(wiki_dir, data_dir, out_individual_f_name)
    out_all_file_path = path.join(wiki_dir, data_dir, out_all_f_name)

    return in_file_path, out_individual_file_path, out_all_file_path



def get_unigram_lm_score_of_query_for_doc(word, individualDocCounter, allDocsCounter, mu=g_mu):
    """
    param word: string
    param: individualDocCounter: Counter containing the word frequencies of each word in a doc 
    param: allDocsCounter: Counter containing the word frequencies of each word in the entire corpus 
    return: relevalce score
    """


    totalNumOfWordsInDoc = sum(individualDocCounter.values())
    p_q_d = individualDocCounter[word]/totalNumOfWordsInDoc

    smoothing = totalNumOfWordsInDoc/(mu + totalNumOfWordsInDoc)

    if word not in allDocsCounter:  
        #print("allDocsCounter[{}] = 0".format(word))
        return 0
    
    totalNumOfWordsInCollection = sum(allDocsCounter.values())
    p_q_c = allDocsCounter[word]/totalNumOfWordsInCollection

    s = smoothing * p_q_d + (1 - smoothing) * p_q_c
    return np.log(s)


def main():
    
    in_file_path, out_individual_file_path, out_all_file_path = get_input_and_output_data_file_names(g_wikiclir2018_dir, 
                                                                                                     g_query_wikiclir2018_language, 
                                                                                                     g_doc_wikiclir2018_language, 
                                                                                                     g_data_mode_to_f_name[g_data_mode])


    # 1) Read data from the raw file
    # 2) Process the raw data (both query and document)
    # 3) Store the counts of words (as counters)
    # 4) The word counts for each sample is stored in out_individual_file_path
    #    and the word counts aggregated over all documents (not for queries) is stored in out_all_file_path 
    data.process_and_store_data(in_file_path, out_individual_file_path, out_all_file_path,
                                g_wikiclir2018_language_to_nltk_language[g_query_wikiclir2018_language], 
                                g_wikiclir2018_language_to_nltk_language[g_doc_wikiclir2018_language], 
                                True,
                                g_max_samples)



    doc_emb = embeddings.Embeddings(g_doc_embeddings_file, "french")
    query_emb = embeddings.Embeddings(g_query_embeddings_file, "english")
    translator = embeddings.WordTranslator(query_emb, doc_emb, g_KNN_K)

    allDocsCounter = None
    with open(out_all_file_path, 'rb') as f:
        allDocsCounter = pickle.load(f)

    for relQueryDoc in data.load_all_pickled_data(out_individual_file_path):
        relScore = 0
        for qToken in relQueryDoc.query:
            # Translate query token (that is qToken) from source language to target language. 
            # Note that translated_words_for_qToken is a list with length = g_KNN_K
            translated_words_for_qToken = translator.get_translations(qToken)

            if get_unigram_lm_score_of_query_for_doc:
                # From translated words, pick the most relevant translation, i.e. translated_words_for_qToken[0]
                # For translated_words_for_qToken[0][0], find its relevance score via unigram language model. 
                relScore += get_unigram_lm_score_of_query_for_doc(translated_words_for_qToken[0][0], 
                                                                  relQueryDoc.doc, 
                                                                  allDocsCounter)
            else: 
                raise Exception("get_unigram_lm_score_of_query_for_doc==False not implemented")

        print("relScore = {}, actualRel = {} docId = {}".format(relScore, relQueryDoc.relevance, relQueryDoc.doc_idx))
            
if __name__=="__main__":
    main()
    sys.exit(0)
