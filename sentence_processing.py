import spacy
import json
import os

nlp = spacy.load('en')
PATH = os.getcwd()
sentences = []

with open(PATH + '//data//sentences.json', 'r+') as fp:
    sentences = json.load(fp)


proc_sen = []

c = 0
for sen in sentences:
    c += 1
    if c % 100 == 0:
        print(c)

    spacy_ob = nlp(sen)
    temp_ob = []
    for token in spacy_ob:
        if token.lemma_ == '-PRON-':
            temp_ob.append((token.text, token.text, token.tag_))
        else:
            temp_ob.append((token.text, token.lemma_, token.tag_))

    proc_sen.append(temp_ob)

with open(PATH + '//data//proc_sen.json', 'w+') as fp:
    json.dump(proc_sen, fp)
