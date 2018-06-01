import pylangacq as pyl
import os
import json


def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


PATH = os.getcwd()

with open(PATH + '\\data\\not_char.json', 'r') as fp:
    not_char = json.load(fp)

sentences = []

for file in os.listdir(PATH + '\\data\\CHAT_Files'):
    print("processing file : " + file)
    if file.endswith('.cha'):
        chat_data = pyl.read_chat(PATH + '\\data\\CHAT_Files\\' + file)
        sen_data = chat_data.sents()

        for sen in sen_data:
            temp_sent = ""
            for word in sen:
                w = word.lower()
                for nc in not_char:
                    w = w.replace(nc, '')
                if w != '':
                    if not (len(set(w)) == 1 and 'x' in set(w)):
                        temp_sent += w + ' '
            tsen = temp_sent[:-1]

            if tsen != '':
                sentences.append(tsen)


sen = remove_duplicates(sentences)

with open(PATH + '\\data\\sentences.json', 'w+') as fp:
    json.dump(sen, fp)

with open(PATH + '\\data\\sentences.txt', 'w+') as fp:
    for s in sen:
        fp.write(s + '\n')
