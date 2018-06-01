from collections import defaultdict
import os
import json
from itertools import product


delta = 0.75
sentences = []
PATH = os.getcwd()
req_lemmas = []
trigram_data = dict()
succ_counter = defaultdict(int)
pred_counter = defaultdict(int)
bigram_data = []
Pkn = dict()
total_trigrams = 0


def remap(data_ob):
    return [{'key': k, 'value': v} for k, v in data_ob.items()]


def smoother(word_b, word_pair, trigram_data, succ_counter, Pkn):

    v1 = max(trigram_data[word_pair][word_b] - delta, 0) / succ_counter[word_pair]

    v2 = (delta * len(trigram_data[word_pair]) * Pkn[word_pair[1]][word_b]) / (succ_counter[word_pair])

    return v1 + v2


with open(PATH + '\\data\\proc_sen.json', 'r+') as fp:
    sentences = json.load(fp)

with open(PATH + '\\data\\req_lemmas.json', 'r+') as fp:
    req_lemmas = json.load(fp)

with open(PATH + '\\data\\full_bigram_data.json', 'r+') as fp:
    bigram_data = json.load(fp)

for word_a in bigram_data.keys():
    Pkn[word_a] = dict()
    for word_b in bigram_data[word_a]:
        Pkn[word_a][word_b[1]] = word_b[0]

req_lemmas = set(req_lemmas.keys())

trigram_data[('^', '^')] = defaultdict(int)

for lemma in req_lemmas:
    trigram_data[('^', lemma)] = defaultdict(int)
    trigram_data[(lemma, '$')] = defaultdict(int)

for lemma_a, lemma_b in product(req_lemmas, req_lemmas):
    trigram_data[(lemma_a, lemma_b)] = defaultdict(int)

print('processing sentences')
for sen in sentences:

    if sen[0][1] in req_lemmas:
        trigram_data[('^', '^')][sen[0][1]] += 1
        succ_counter[('^', '^')] += 1

    if len(sen) > 1:
        if sen[0][1] in req_lemmas and sen[1][1] in req_lemmas:
            trigram_data[('^', sen[0][1])][sen[1][1]] += 1
            succ_counter[('^', sen[0][1])] += 1

    for lemma_a, lemma_b, lemma_c in zip(sen, sen[1:], sen[2:]):
        if lemma_a[1] in req_lemmas and lemma_b[1] in req_lemmas and lemma_c[1] in req_lemmas:
            trigram_data[(lemma_a[1], lemma_b[1])][lemma_c[1]] += 1
            succ_counter[(lemma_a[1], lemma_b[1])] += 1

    if len(sen) > 1:
        if sen[-1][1] in req_lemmas and sen[-2][1] in req_lemmas:
            trigram_data[(sen[-2][1], sen[-1][1])]['$'] += 1
            succ_counter[(sen[-2][1], sen[-1][1])] += 1

    #if sen[-1][1] in req_lemmas:
        #trigram_data[(sen[-1][1], '$')]['$'] += 1
        #succ_counter[(sen[-1][1], '$')] += 1
print('finished processing sentences')
req_data = dict()
temp_search_set = req_lemmas
temp_search_set.add('$')
temp_search_set.add('^')


print('processing values')
for word_pair in trigram_data.keys():
    smoothed_data = dict()
    # smoothed_data = bigram_data[word_a]
    for word in trigram_data[word_pair].keys():
        smoothed_data[word] = smoother(word, word_pair, trigram_data, succ_counter, Pkn)

    data = sorted([(smoothed_data[l], l) for l in smoothed_data.keys()], key=lambda x: x[0], reverse=True)

    req_data[word_pair] = data[:40]
print('finished processing values')

print('saving data')
with open(PATH + '\\data\\trigram_data.json', 'w+') as fp:
    final_data = remap(req_data)
    json.dump(final_data, fp)
print('finished saving data')
