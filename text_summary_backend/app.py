import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from bs4 import BeautifulSoup
import requests
import math
import re
from flask import request
from models import Document, Sentence
from text_rank import text_rank
import urllib.parse

from flask import Flask

app = Flask(__name__)

@app.route("/modified_text_rank_summarize",methods = ['POST'])
def modified_text_rank_summarize():
    content = request.get_json()
    soup = BeautifulSoup(content['content'], "html.parser")
    texts = soup.find_all("p")
    doc_str = ''.join([text.text for text in texts])
    document = Document(doc_str)
    res = {'summary': text_rank(document)}
    return res

