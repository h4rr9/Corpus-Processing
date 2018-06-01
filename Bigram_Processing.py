from collections import defaultdict
import os
import json

bigram_data = dict()
succ_counter = defaultdict(int)
pred_counter = defaultdict(int)
delta = 0.75
total_bigrams = 0
sentences = []
req_lemmas = []


def smoother(word_b, word_a, bigram_data, succ_counter, pred_counter, total_bigrams):

    v1 = max(bigram_data[word_a][word_b] - delta, 0) / succ_counter[word_a]

    v2 = (delta * len(bigram_data[word_a]) * pred_counter[word_b]) / (succ_counter[word_a] * total_bigrams)

    return v1 + v2


PATH = os.getcwd()

with open(PATH + '\\data\\proc_sen.json', 'r+') as fp:
    sentences = json.load(fp)

with open(PATH + '\\data\\req_lemmas.json', 'r+') as fp:
    req_lemmas = json.load(fp)

req_lemmas = set(req_lemmas.keys())
bigram_data['^'] = defaultdict(int)
bigram_data['$'] = defaultdict(int)

for lemma in req_lemmas:
    bigram_data[lemma] = defaultdict(int)
    smoothed_data = defaultdict(int)

print('processing sentences')

for sen in sentences:
    if sen[0][1] in req_lemmas:
        bigram_data['^'][sen[0][1]] += 1
        succ_counter['^'] += 1

    for lemma_a, lemma_b in zip(sen, sen[1:]):
        if lemma_a[1] in req_lemmas and lemma_b[1] in req_lemmas:
            bigram_data[lemma_a[1]][lemma_b[1]] += 1
            succ_counter[lemma_a[1]] += 1

    if sen[-1][1] in req_lemmas:
        bigram_data[sen[-1][1]]['$'] += 1
        succ_counter[sen[-1][1]] += 1

print('finished processing sentences')

print('finding values')

for word_a in bigram_data.keys():

    total_bigrams += len(bigram_data[word_a].keys())

    for word_b in bigram_data.keys():
        if word_a in set(bigram_data[word_b].keys()):
            pred_counter[word_a] += 1


print('finished finding values')
print('procesing bigram values')

req_data = dict()

for word_a in bigram_data.keys():

    smoothed_data = dict()
    # smoothed_data = bigram_data[word_a]
    for word_b in bigram_data[word_a].keys():
        smoothed_data[word_b] = smoother(word_b, word_a, bigram_data, succ_counter, pred_counter, total_bigrams)

    data = sorted([(smoothed_data[l], l) for l in smoothed_data.keys()], key=lambda x: x[0], reverse=True)

    req_data[word_a] = data[:40]

print('finished procesing bigram values')

with open(PATH + '\\data\\bigram_data.json', 'w+') as fp:
    json.dump(req_data, fp)
