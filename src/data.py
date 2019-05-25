

class RelevanceQueryDoc:
    def __init__(self, relevance, query, doc):
        self.relevance = relevance
        self.query = query
        self.doc = doc


def get_data(file_path, max_queries=None, delimiter='\t'):
    '''
    param file_path: path to the data file. The format for the content of the file is:
                     relevance\delimiter\query\delimiter\document.
    param max_queries: Max number of examples to be gotten. Helpful while debugging.
    param delimiter: the delimiter which is used to separate out the relevance/query/doc on each line of the file. 
    returns: yields object RelevanceQueryDoc
    '''

    with open(file_path, 'r', encoding='utf-8', newline='\n', errors='ignore') as f:
        for idx, line in enumerate(f):
            
            if max_queries is not None:
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

