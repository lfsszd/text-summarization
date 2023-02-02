import re
import math
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(nltk.corpus.stopwords.words("english"))

class Sentence(object):
    def __init__(self, id, sentence, document):
        words = word_tokenize(sentence)
        # The paper didn't mention it, but I think we should remove punctuation marks too.
        words_after_removing_stop_words = [word.lower() for word in words if word not in stop_words and re.match('\w+', word)]
        self.id = id
        self.original = sentence
        self.words = words_after_removing_stop_words
        self.words_set = set(self.words)
        self.word_counts = {}
        self.document = document
        for word in self.words:
            self.word_counts[word] = self.word_counts.get(word, 0) + 1

    def tf(self, word):
        return self.word_counts.get(word, 0)

    def norm(self):
        res = 0
        for word in self.words_set:
            res += (self.tf(word) * self.document.isf.get(word, 1)) ** 2
        return res ** 0.5

    @staticmethod
    def weight(s1, s2):
        numerator = 0
        for word in s1.words_set.union(s2.words_set):
            numerator += s1.tf(word) * s2.tf(word) * (s1.document.isf.get(word, 1) ** 2)
        demonimator = s1.norm() * s2.norm()
        if demonimator == 0:
            return 0
        return numerator/demonimator


class Document(object):
    def __init__(self, doc_str):
        self.doc_str = doc_str
        document = re.sub(r'\s+', ' ', doc_str)
        self.all_words = word_tokenize(document.lower())
        self.all_words = set([word for word in self.all_words if word not in stop_words and re.match('\w+', word)])
        self.all_word_counts = {}
        self.sentences = self.process_sentences()
        self.isf = {}
        for sentence in self.sentences.values():
            for word in sentence.words_set:
                self.all_word_counts[word] = self.all_word_counts.get(word, 0) + 1

        for word, ct in self.all_word_counts.items():
            self.isf[word] = math.log(len(self.sentences)) - math.log(ct)



    def process_sentences(self):
        sentences = sent_tokenize(self.doc_str)
        sentence_objects = {}
        for index, sentence_str in enumerate(sentences):
            sentence = Sentence(index, sentence_str, self)
            sentence_objects[sentence.id] = sentence

        return sentence_objects
