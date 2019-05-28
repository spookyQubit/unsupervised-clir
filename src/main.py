import sys
import os
from os import path
import pickle
from collections import Counter

import data


g_wikiclir2018_dir = "../Data/wikiclir2018"
g_query_wikiclir2018_language = "en"
g_doc_wikiclir2018_languages = ["fr"]

# required for stopwords
g_wikiclir2018_language_to_nltk_language = {"en": "english", 
                                            "fr": "french", 
                                            "ja": "japanese"}  
g_data_mode = 'dev'
g_data_mode_to_f_name = {'dev': 'dev', 'test': 'test1', 'train': 'train'}
g_max_samples = 100000


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
             out_individual_file_path is the file where to store processed data for each docment
             out_all_file_path is the file where to store processed data for all doucument 
    '''

    data_dir = '_'.join(['data', query_wiki_lang, doc_wiki_lang])

    in_f_name = f_name + '.txt'
    out_individual_f_name = f_name + '_individual_processed' + '.txt'
    out_all_f_name = f_name + '_all_processed' + '.txt'
    
    in_file_path = path.join(wiki_dir, data_dir, in_f_name)
    out_individual_file_path = path.join(wiki_dir, data_dir, out_individual_f_name)
    out_all_file_path = path.join(wiki_dir, data_dir, out_all_f_name)

    return in_file_path, out_individual_file_path, out_all_file_path


def process_and_store_data(input_file, output_individual_file, output_all_file,
                           query_lang, doc_lang, 
                           generate_output_file_from_scratch=True,
                           max_samples=None):

    if not path.exists(input_file):
        raise Exception("{} does not exist".format(input_file))

    '''
    Check if the output_file already exists. 
    If it already exists, check how many entries are there.
    If the number of entries are the same as the number of entries in input_file, 
    do not do anything.
    '''

    queryProcessor = data.TextProcessor(query_lang) 
    docProcessor = data.TextProcessor(doc_lang) 

    all_docs_counter = Counter()
    individual_doc_counter = Counter()
    individual_query_counter = Counter()
    
    if generate_output_file_from_scratch: 
        if path.exists(output_individual_file):
            os.remove(output_individual_file)
    
        if path.exists(output_all_file):
            os.remove(output_all_file)
    
    with open(output_individual_file, "wb") as out_individual_file:
        for loaded_data in data.get_data(input_file, max_samples):
            processed_query = queryProcessor.clean_and_tokenize(loaded_data.query)
            processed_doc = docProcessor.clean_and_tokenize(loaded_data.doc)

            # Clear and update individual_doc_counter
            individual_doc_counter.clear()
            individual_doc_counter.update(processed_doc) 

            # Update all_doc_counter
            all_docs_counter.update(individual_doc_counter)
        
            # Clear and update individual_query_counter
            individual_query_counter.clear()
            individual_query_counter.update(processed_query)

            pickle.dump(data.RelevanceQueryDoc(loaded_data.relevance, 
                                               individual_query_counter, 
                                               individual_doc_counter, 
                                               loaded_data.doc_idx), out_individual_file)

    with open(output_all_file, "wb") as out_all_file:
        pickle.dump(all_docs_counter, out_all_file)


def main():
    # load word embeddings
    # load documents query in chunks
    # prepare a file to write results to
    # process query and texts
    # run experiment 

    for doc_wiki_lang in g_doc_wikiclir2018_languages:
        in_file_path, out_individual_file_path, out_all_file_path = get_input_and_output_data_file_names(g_wikiclir2018_dir, 
                                                                                                         g_query_wikiclir2018_language, 
                                                                                                         doc_wiki_lang, 
                                                                                                         g_data_mode_to_f_name[g_data_mode])

        process_and_store_data(in_file_path, out_individual_file_path, out_all_file_path,
                               g_wikiclir2018_language_to_nltk_language[g_query_wikiclir2018_language], 
                               g_wikiclir2018_language_to_nltk_language[doc_wiki_lang], 
                               True,
                               g_max_samples)


if __name__=="__main__":
    main()
    sys.exit(0)
