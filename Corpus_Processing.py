from Books import book1, book4, book5
import json
import os

word_list1 = []
word_list2 = []

Test = []
PATH = os.getcwd()

with open(PATH + '\\data\\proc_sen.json', 'r+') as fp:
    Test = json.load(fp)

print('generating word lists')
word_config = []
with open(PATH + '\\data\\req_lemmas.json', 'r+') as fp:
    word_config = json.load(fp)
print('finished generating word configs')
print('generating books')

Book1 = book1(50, 40, word_config)
Book2 = book4(50, 40, word_config)
Book3 = book5(50, 40, word_config)

print('finished generating books')
