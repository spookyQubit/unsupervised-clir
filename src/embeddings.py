import numpy as np

def load_embeddings(file_path, delimiter = ' '):
    
    '''
    param file_path: path to the embedding file. The format for the content of the file is:
                     word\delimiter\f_1\delimiter\f_2\delimiter\f_dim 
                     where dim is the dimension of the embedding vector.
    param delimiter: the delimiter which is used to separate out the word/vec_values on each line of the file. 
    returns        : dim: dimension of the word vectors
                     word2id: dict from word to word index 
                     id2word: dict from word index to word 
                     embeddings: np.vstack(vectors) which are numpy vector of shape (len(word2id), dim)
    '''

    vectors = []
    word2id = {}
    id2word = {}
    dim = -1
    is_dim_set = False
    with open(file_path, 'r', encoding='utf-8', newline='\n', errors='ignore') as f:
    
        # Skip the first line as that contains the number oof words and the dinsion information
        next(f)
    
        for line in f:
            tokens = line.split(delimiter)

            word = ""
            try:
                word = tokens[0]
            except:
                raise Exception('Got an empty list after splitting the line with delimiter {}'.format(delimiter))

            if word in word2id:
                raise Exception('Word {} found multiple times'.format(word))
        
            vec = []
            try:
                vec = [float(val) for val in tokens[1:]]
            except:
                raise Exception('Cannot read the vector of word {} in float format'.format(word))

            if is_dim_set:
                if dim != len(vec):
                    raise Exception("The dimension for word {0} is {1}, which is different than previously seen dimension of {2}".format(word, len(vec), dim))
            else:
                dim = len(vec)
                is_dim_set = True

            vectors.append(vec)
            word2id[word] = len(word2id)
            id2word[word2id[word]] = word

        return dim, word2id, id2word, np.vstack(vectors)


def get_knn(src_word, src_emb, src_id2word, trg_emb, trg_id2word, K=5):
    '''
    param src_word: A word (string) in the source language.   
    param src_emb: Source word embeddings (numpy matrix of shape (vocab_size, emb_dimension))
    param src_id2word: Dict {id: word in source language} 
    param trg_emb: Target word embeddings (numpy matrix of shape (vocab_size, emb_dimension))
    param trg_id2word: Dict {id: word in target language}
    param K: Number of nearest neighbours  
    returns: knn_trg_ids: Ids of words (list) in target language which are nearest to src_word
             knn_scores_of_trg_ids: Scores (list) measuring nearness between src_word embedding and knn target words 
     

    '''
    src_word2id = {v:k for k, v in src_id2word.items()}
    src_word_emb = src_emb[src_word2id[src_word]]
    scores = ( trg_emb / np.linalg.norm(trg_emb, 2, 1)[:, None] ).dot(src_word_emb/np.linalg.norm(src_word_emb))
    knn_trg_ids = scores.argsort()[-K:][::-1]
    knn_scores_of_trg_ids = [scores[idx] for idx in knn_trg_ids]

    return knn_trg_ids, knn_scores_of_trg_ids 


class Embeddings:

    def __init__(self, file_path, lang, delimiter = ' '):
       self.file_path = file_path
       self.language = lang
       self.delimiter = delimiter

       self.dim, self.word2id, self.id2word, self.embeddings = load_embeddings(file_path, delimiter)
