import sys
from os import path

g_wikiclir2018_dir = "../Data/wikiclir2018"
g_query_wikiclir2018_language = "en"
g_doc_wikiclir2018_languages = ["fr", "ja"]

# required for stopwords
g_wikiclir2018_language_to_nltk_language = {"en": "english", 
                                            "fr": "french", 
                                            "ja": "japanese"}  
g_data_mode = 'dev'
g_data_mode_to_f_name = {'dev': 'dev', 'test': 'test1', 'train': 'train'}


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
    returns: in_file_path, that is the file from which to read data
             out_file_path, that is the file where to store processed data
    '''

    data_dir = '_'.join(['data', query_wiki_lang, doc_wiki_lang])

    in_f_name = f_name + '.txt'
    out_f_name = f_name + '_processed' + '.txt'
    
    in_file_path = path.join(wiki_dir, data_dir, in_f_name)
    out_file_path = path.join(wiki_dir, data_dir, out_f_name)

    return in_file_path, out_file_path


def process_and_store_data(input_file, output_file, query_lang, doc_lang):

    if not path.exists(input_file):
        raise Exception("{} does not exist".format(input_file))




def main():
    # load word embeddings
    # load documents query in chunks
    # prepare a file to write results to
    # process query and texts
    # run experiment 

    for doc_wiki_lang in g_doc_wikiclir2018_languages:
        in_file_path, out_file_path = get_input_and_output_data_file_names(g_wikiclir2018_dir, 
                                                                           g_query_wikiclir2018_language, 
                                                                           doc_wiki_lang, 
                                                                           g_data_mode_to_f_name[g_data_mode])

        process_and_store_data(in_file_path, out_file_path, 
                               query_lang=g_wikiclir2018_language_to_nltk_language[g_query_wikiclir2018_language], 
                               doc_lang=g_wikiclir2018_language_to_nltk_language[doc_wiki_lang])


if __name__=="__main__":
    main()
    sys.exit(0)
