import spacy
import json
import os
from collections import defaultdict

nlp = spacy.load('en')
PATH = os.getcwd()
sentences = []


with open(PATH + '\\data\\proc_sen.json', 'r+')as fp:
    proc_sen = json.load(fp)

uniq_words = set()
count_lemma = defaultdict(int)

c = 0
for sen in proc_sen:
    c += 1
    if c % 100 == 0:
        print(c)
    for token in sen:
        uniq_words.add(token[1])

with open(PATH + '\\data\\uniq_words.json', 'w+') as fp:
    json.dump(list(uniq_words), fp)

with open(PATH + '\\data\\uniq_words.txt', 'w+') as fp:
    for w in uniq_words:
        fp.write(w + '\n')
