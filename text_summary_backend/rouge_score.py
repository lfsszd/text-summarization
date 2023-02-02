import re
from text_rank import text_rank
from models import Document, Sentence
from datasets import load_dataset
from nltk.tokenize import word_tokenize
import torch

data_set = load_dataset('cnn_dailymail', '3.0.0')
validate_set = data_set['validation']
# print(len(validate_set))
recalls = []
precisions = []
f1_scores = []
ct = 0

for data in validate_set:
    ct += 1
    words = word_tokenize(data['highlights'])
    heighlights = set([word for word in words if re.match('\w+', word)])

    document = Document(data['article'])
    try:
        summary = text_rank(document)
    except Exception as e:
        print('error')
        print(data['id'])
        raise e
    summary = set([word for word in word_tokenize(summary) if re.match('\w+', word)])

    tp = summary.intersection(heighlights)
    fp = summary - heighlights
    fn = heighlights - summary
    recall = (0.0 + len(tp)) / (len(tp) + len(fn))
    try:
        precision = (0.0 + len(tp)) / (len(tp) + len(fp))
    except:
        print('err')
        print('len(tp)')
        print(len(tp))
        print('len(fp)')
        print(len(fp))
        print('len(fn)')
        print(len(fn))
        print('heighlights')
        print(data['highlights'])
        summary = text_rank(document)
        print('summary')
        print(summary)
        print(data['id'])
        exit()
        
    if recall + precision:
        f1_score = (0.0 + 2 * precision * recall)/(precision + recall)
    else:
        f1_score = 0.0

    if f1_score > 0.7:
        print('f1_score > 0.7')
        print('len(tp)')
        print(len(tp))
        print('len(fp)')
        print(len(fp))
        print('len(fn)')
        print(len(fn))
        print('heighlights')
        print(data['highlights'])
        summary = text_rank(document)
        print('summary')
        print(summary)
        print(data['id'])


    recalls.append(recall)
    precisions.append(precision)
    f1_scores.append(f1_score)
    if ct % 100 == 0:
        print(ct)


print('average recall:')
print(torch.tensor(recalls).mean())
print('average precision:')
print(torch.tensor(precisions).mean())
print('average f1_score:')
print(torch.tensor(f1_scores).mean())

