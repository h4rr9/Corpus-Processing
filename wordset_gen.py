from collections import defaultdict
from math import inf
import json
import spacy
import os

PATH = os.getcwd()

nlp = spacy.load('en')

lemma_count = defaultdict(int)
proc_sen = []
uniq_words = []
with open(PATH + '//data//proc_sen.json', 'r+') as fp:
    proc_sen = json.load(fp)

with open(PATH + '//data//uniq_words.json', 'r+') as fp:
    uniq_words = json.load(fp)
c = 0
for sen in proc_sen:
    c += 1
    if c % 100 == 0:
        print(c)
    for token in sen:
        lemma_count[token[1]] += 1


print(len(lemma_count))
prev_lemma = ''
while True:
    if len(lemma_count) <= 2000:
        break
    else:
        # if(len(lemma_count)%100 == 0):
        print(len(lemma_count))
        min_lemma = ''
        minv = inf
        minr = ''
        for lemma in lemma_count:
            if lemma_count[lemma] < minv:
                minv = lemma_count[lemma]
                min_lemma = lemma

        temp = []
        # if(len(lemma_count)%100 == 0):
        print('deleting: ' + min_lemma + ' ' + str(minv))
        if prev_lemma == min_lemma:
            print("!!!ERROR!!!")
            break

        for sen in proc_sen:
            temp_lemma_set = set()
            for token in sen:
                temp_lemma_set.add(token[1])

            if min_lemma in temp_lemma_set:
                for token in sen:
                    lemma_count[token[1]] -= 1
                    if lemma_count[token[1]] <= 0:
                        del lemma_count[token[1]]
            else:
                temp.append(sen)

        proc_sen = temp[::]
        prev_lemma = min_lemma


with open(PATH + '//data//req_lemmas.json', 'w+') as fp:
    json.dump(lemma_count, fp)
