from collections import defaultdict
import os
import json
from itertools import product


def remap(data):
    return [{'key': k, 'value': v} for k, v in data.items()]


sentences = []
PATH = os.getcwd()
req_lemmas = []


with open(PATH + '\\data\\proc_sen.json', 'r+') as fp:
    sentences = json.load(fp)

with open(PATH + '\\data\\req_lemmas.json', 'r+') as fp:
    req_lemmas = json.load(fp)

trigram_data = dict()
req_lemmas = set(req_lemmas.keys())

trigram_data[('^', '^')] = defaultdict(int)

for lemma in req_lemmas:
    trigram_data[('^', lemma)] = defaultdict(int)
    trigram_data[(lemma, '$')] = defaultdict(int)

for lemma_a, lemma_b in product(req_lemmas, req_lemmas):
    trigram_data[(lemma_a, lemma_b)] = defaultdict(int)

c = 0
for sen in sentences:
    c += 1
    print(c)
    if sen[0][1] in req_lemmas:
        trigram_data[('^', '^')][sen[0][1]] += 1

    if len(sen) > 1:
        if sen[0][1] in req_lemmas and sen[1][1]:
            trigram_data[('^', sen[0][1])][sen[1][1]] += 1

    for lemma_a, lemma_b, lemma_c in zip(sen, sen[1:], sen[2:]):
        if lemma_a[1] in req_lemmas and lemma_b[1] in req_lemmas and lemma_c[1] in req_lemmas:
            trigram_data[(lemma_a[1], lemma_b[1])][lemma_c[1]] += 1

    if len(sen) > 1:
        if sen[-1][1] in req_lemmas and sen[-2][1] in req_lemmas:
            trigram_data[(sen[-2][1], sen[-1][1])]['$'] += 1

    if sen[-1][1] in req_lemmas:
        trigram_data[(sen[-1][1], '$')]['$'] += 1

req_data = dict()

for key in trigram_data.keys():
    succ_count = trigram_data[key]

    data = sorted([(succ_count[l], l) for l in succ_count.keys()], key=lambda x: x[0], reverse=True)

    req_data[key] = data[:40]

with open(PATH + '\\data\\trigram_data.json', 'w+') as fp:
    json.dump(remap(req_data), fp)
