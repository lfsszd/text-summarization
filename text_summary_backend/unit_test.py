import re
from text_rank import text_rank, construct_weight, scoring, DAMPING_FACTOR
from models import Document, Sentence
from datasets import load_dataset
from nltk.tokenize import word_tokenize
import torch
from pprint import pprint


def assert_equal(a, b):
    try:
        if type(a) == float:
            assert abs(a - b) < abs(a) * 1e-5 or abs(a - b) < 1e-5
        else:
            assert a==b
    except Exception as e:
        print(e)
        print(a)
        print(b)
        raise e


# Test 1
print('test case 1:')
doc_str = '''
Sam likes skiing. 
Skiing is fun. 
Sam likes fun skiing. 
'''
print(doc_str)

document = Document(doc_str)
# pprint([s.words for s in document.sentences.values()])

assert_equal(0.4054651081, document.isf['fun'])
assert_equal(0.4054651081, document.isf['sam'])
assert_equal(0.4054651081, document.isf['likes'])
assert_equal(0, document.isf['skiing'])

assert_equal(0.57341425495, document.sentences[0].norm())
assert_equal(0.40546510815, document.sentences[1].norm())
assert_equal(0.70228616794, document.sentences[2].norm())

assert_equal(0.0, Sentence.weight(document.sentences[1], document.sentences[0]))
assert_equal(0.57735026919, Sentence.weight(document.sentences[1], document.sentences[2]))
assert_equal(0.81649658092, Sentence.weight(document.sentences[0], document.sentences[2]))


assert_equal(0.0, construct_weight(document)[0][1])
assert_equal(0.0, construct_weight(document)[1][1])
assert_equal(0.57735026919, construct_weight(document)[1][2])
assert_equal(0.81649658092, construct_weight(document)[0][2])

final_scores = scoring(document)
assert_equal(0.81649658092 * (1 - DAMPING_FACTOR) + 3.0 * DAMPING_FACTOR, final_scores[0])
assert_equal(0.0 * (1 - DAMPING_FACTOR) + 3.0 * DAMPING_FACTOR, final_scores[1])
assert_equal(0.81649658092 * (1 - DAMPING_FACTOR) + 3.0 * DAMPING_FACTOR, final_scores[2])

print('passed')
# Test 2
print('test case 2:')
doc_str = '''1 2 3 4. 
1 3 5. 
1 2 2 5. 
1 2 3 4 5. 
'''
print(doc_str)

document = Document(doc_str)
# pprint([s.words for s in document.sentences.values()])
# pprint(text_rank(document))
# print(document.isf)


assert_equal(0, document.isf['1'])
assert_equal(0.28768207245, document.isf['2'])
assert_equal(0.28768207245, document.isf['3'])
assert_equal(0.69314718056, document.isf['4'])
assert_equal(0.28768207245, document.isf['5'])


assert_equal(0.80372567679, document.sentences[0].norm())
assert_equal(0.40684388851, document.sentences[1].norm())
assert_equal(0.64327666991, document.sentences[2].norm())
assert_equal(0.85366031789, document.sentences[3].norm())

assert_equal(0.25309872526, Sentence.weight(document.sentences[1], document.sentences[0]))
assert_equal(0.31622776601, Sentence.weight(document.sentences[1], document.sentences[2]))
assert_equal(0.32014737788, Sentence.weight(document.sentences[0], document.sentences[2]))
assert_equal(0.94150525678, Sentence.weight(document.sentences[3], document.sentences[0]))
assert_equal(0.47658756063, Sentence.weight(document.sentences[3], document.sentences[1]))
assert_equal(0.45213065883, Sentence.weight(document.sentences[3], document.sentences[2]))

average_weight = (0.25309872526 + 0.31622776601 + 0.32014737788 + 0.94150525678 + 0.47658756063 + 0.45213065883) / 6

0.45994955756499994
initial_costs = [
    (0 + 0.0 + 0.94150525678) / 1,
    (0.0 + 0.0 + 0.47658756063),
    (0.0 + 0.0 + 0.0),
    (0.0 + 0.47658756063 + 0.94150525678) / 2,
]


final_scores = scoring(document)
assert_equal((initial_costs[1] + initial_costs[0])/2 * (1 - DAMPING_FACTOR) + 4.0 * DAMPING_FACTOR, final_scores[3])
assert_equal(0 * (1 - DAMPING_FACTOR) + 4.0 * DAMPING_FACTOR, final_scores[2])
assert_equal(initial_costs[3] * (1 - DAMPING_FACTOR) + 4.0 * DAMPING_FACTOR, final_scores[1])
assert_equal(initial_costs[3] * (1 - DAMPING_FACTOR) + 4.0 * DAMPING_FACTOR, final_scores[0])

print('passed')
print('all passed!')
