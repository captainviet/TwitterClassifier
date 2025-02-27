import string

from nltk.corpus import stopwords as sw
from nltk.corpus import wordnet as wn
from nltk import wordpunct_tokenize
from nltk import WordNetLemmatizer
from nltk import sent_tokenize
from nltk import pos_tag

from sklearn.preprocessing import LabelEncoder
from sklearn.base import BaseEstimator, TransformerMixin


class Preprocessor(BaseEstimator, TransformerMixin):
    
    def __init__(self, stopwords=None, punct=None, lower=True, strip=True):
        self.stopwords = set(stopwords) if stopwords else set(sw.words('english'))
        self.punct = punct if punct else set(string.punctuation)
        self.lower = lower
        self.strip = strip 
        self.lemmatizer = WordNetLemmatizer()
    
    def fit(self, X, y=None):
        return self
    
    def inverse_transform(self, X):
        return X
    
    def transform(self, X):
        return [
            list(self.tokenize(doc)) for doc in X
        ]
    
    def tokenize(self, document):
        """
        Returns a normalized, lemmatized list of tokens from a document by
        applying segmentation (breaking into sentences), then word/punctuation
        tokenization, and finally part of speech tagging. It uses the part of
        speech tags to look up the lemma in WordNet, and returns the lowercase
        version of all the words, removing stopwords and punctuation.
        """
        # Break the document into sentences
        for sentence in sent_tokenize(document):
            # Break the sentence into part of speech tagged token
            for token, tag in pos_tag(wordpunct_tokenize(sentence)):
                # Applying preprocessing to the token
                token = token.lower() if self.lower else token
                token = token.strip() if self.strip else token 
                token = token.strip('_') if self.strip else token 
                token = token.strip('*') if self.strip else token 
            
                # If punctuation of stopword, ignore the token and continue
                if token in self.stopwords or all(char in self.punct for char in token):
                    continue
                
                # Lemmatize the token and yield
                lemma = self.lemmatize(token, tag)
                
                yield lemma
            
    def lemmatize(self, token, tag):
        """
        Converts the Penn Treebank tag to a WordNet POS tag, then uses that
        tag to perform much more accurate WordNet lemmatization.
        """
        tag = {
            'N': wn.NOUN,
            'V': wn.VERB,
            'R': wn.ADV,
            'J': wn.ADJ
        }.get(tag[0], wn.NOUN)
        
        return self.lemmatizer.lemmatize(token, tag)
    
    