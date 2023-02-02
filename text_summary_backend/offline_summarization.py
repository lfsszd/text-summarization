import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from bs4 import BeautifulSoup
import requests
import math
import re

from models import Document, Sentence
from text_rank import text_rank

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

URL = "https://www.cnn.com/interactive/2022/12/us/el-paso-crossings-migrant-stories-reaj-cnnphotos/"
URL = "https://www.bbc.com/news/uk-england-kent-64017542"
URL = "https://www.cnn.com/2022/12/15/health/hospital-misdiagnoses-study"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
texts = soup.find_all("p")

doc_str = ''.join([text.text for text in texts])
document = Document(doc_str)

# documents = re.sub(r'\s+', ' ', documents)


for sentence in document.sentences.values():
    print(sentence.original)
    print(' ')


print('Summary result')
print(text_rank(document))
print(' ')
# stopwords = set(stopwords.words("english"))
# print(stopwords)
# all_words = word_tokenize(document)
# all_words = set([word for word in all_words if word not in stopwords and re.match('\w+', word)])

# all_word_counts = {}

# for word in all_words:
#     all_word_counts[word] = all_word_counts.get(word, 0) + 1

