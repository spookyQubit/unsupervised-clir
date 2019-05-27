import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class RelevanceQueryDoc:
    def __init__(self, relevance, query, doc):
        self.relevance = relevance
        self.query = query
        self.doc = doc


class TextProcessor:
    
    def __init__(self, lang):
        self.lang = lang
        try:
            self.stopwords = set(stopwords.words(self.lang))
        except:
            raise ValueError("Do not support for language={} to get stopwords".format(self.lang)) 

        self.punctuation_translate_table = str.maketrans({key: None for key in string.punctuation})
    
    def clean(self, in_str):
        '''
        param in_str: input string.
        returns: A string with the following transformations: 
                 1) converts to lower
                 2) Removes '\r'
                 3) Removes '\n'
                 4) Removes '\t'
                 5) Removes punctuations
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
    returns: yield one instance of RelevanceQueryDoc
    '''

    with open(file_path, 'r', encoding='utf-8', newline='\n', errors='ignore') as f:
        for idx, line in enumerate(f):
            
            if max_samples is not None:
                if idx >= max_queries:
                    break

            tokens = line.split(delimiter)

            if len(tokens) != 3:
                raise Exception("Data is not in the format of relevance\delimiter\query\delimiter\document")
            
            relevance = -1        
            try:
                relevance = int(tokens[0])
            except:
                raise Exception('Could not get relevance after splitting the line with delimiter {}'.format(delimiter))

            query = tokens[1] 
            doc = tokens[2]

            yield RelevanceQueryDoc(relevance, query, doc)

