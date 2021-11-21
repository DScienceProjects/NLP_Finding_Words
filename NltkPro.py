import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from logger_class import Logger
import Constants

log = Logger("MaintenancePrediction")


class NltkProcessing:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemitizer = WordNetLemmatizer()

    def process(self, desc):
        try:
            sentence = nltk.sent_tokenize(desc)
            corpus = []
            for i in range(len(sentence)):
                words = re.sub('[^a-zA-Z]', " ", sentence[i])
                words = words.lower()

                words = words.split()
                word = [self.lemitizer.lemmatize(word) for word in words if word not in set(stopwords.words('english'))]
                sentence[i] = ' '.join(words)
                corpus.append(word)

            l = []
            for i in range(len(corpus)):
                for d in range(len(corpus[i])):
                    l.append(corpus[i][d])
        except Exception as e:
            log.add_exception_log(Constants.EXCEPTION_HANDLING + " NltkProcessing process() " + e)
        return set(l)
