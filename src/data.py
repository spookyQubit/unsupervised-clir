import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class RelevanceQueryDoc:
    def __init__(self, relevance, query, doc, doc_idx):
        self.relevance = relevance
        self.query = query
        self.doc = doc
        self.doc_idx = doc_idx


class TextProcessor:
    
    def __init__(self, lang):
        self.lang = lang
        try:
            self.stopwords = set(stopwords.words(self.lang))
        except:
            raise ValueError("Do not support for language={} to get stopwords".format(self.lang)) 

        self.punctuation_translate_table = str.maketrans({key: ' ' for key in string.punctuation})
    
    def clean(self, in_str):
        '''
        param in_str: input string.
        returns: A string with the following transformations: 
                 1) converts to lower
                 2) Replaces '\r' with ' '
                 3) Replaces '\n' with ' '
                 4) Replaces '\t' with ' '
                 5) Replaces punctuations with ' '
                 6) Remove leading and trailing white spaces
        '''
        # Convert the string to lower case
        clean_str = in_str.lower()

        # Remove \r char
        clean_str = clean_str.replace('\r', ' ')
    
        # Remove \n char
        clean_str = clean_str.replace('\n', ' ')

        # Remove \t char
        clean_str = clean_str.replace('\t', ' ')
        
        # Remove punctuations
        clean_str = clean_str.translate(self.punctuation_translate_table)

        # Remove leading and trailing white spaces
        clean_str = clean_str.strip() 

        return clean_str

    def tokenize(self, text):
        
        tokens = []
        for token in word_tokenize(text, language=self.lang):
            if token not in self.stopwords:
                tokens.append(token)
        return tokens

    def clean_and_tokenize(self, in_str):
        clean_str = self.clean(in_str)
        return self.tokenize(clean_str)


def get_data(file_path, max_samples=None, delimiter='\t'):
    '''
    param file_path: path to the data file. The format for the content of the file is:
                     relevance\delimiter\query\delimiter\document.
    param max_samples: Max number of examples to be gotten. Helpful while debugging.
    param delimiter: the delimiter which is used to separate out the relevance/query/doc on each line of the file. 
    returns: yield one instance of RelevanceQueryDoc.
             Make sure no exceptions are raised inside this generator because 
             when a generator throws an exception, it exits. 
             One can't continue consuming the items it generates after generator raises exception. 
    '''

    with open(file_path, 'r', encoding='utf-8', newline='\n', errors='ignore') as f:
        for idx, line in enumerate(f): 

            relevance = -1
            query = ""
            doc = ""

            if max_samples is not None:
                if idx >= max_samples:
                    break

            tokens = line.split(delimiter)

            if len(tokens) != 3:
                print("Data is not in the format of relevance\delimiter\query\delimiter\document")
            else:    
                try:
                    relevance = int(tokens[0])
                    query = tokens[1] 
                    doc = tokens[2]
                except:
                    print('Could not get relevance/query/doc after splitting the line with delimiter {}'.format(delimiter))
                
            yield RelevanceQueryDoc(relevance, query, doc, idx)

