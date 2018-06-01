from operator import itemgetter
import os
import json
import nltk


PATH = os.getcwd()


class configuration:

    def __init__(self, nop, wpp, words):
        self.pages = []

        for i in range(0, nop * wpp, wpp):
            self.pages.append(words[i:i + wpp])

        self.number_pages = nop
        self.words_per_page = wpp
        self.word_set = set(words)

    def get_nop(self):
        return self.number_pages

    def get_page(self, n):
        return self.pages[n]

    def test_senct(self, senct):
        for token in senct:
            if token[1] not in self.word_set:
                return False
        return True

    def in_page(self, word, n):
        if word in self.get_page(n):
            return True
        else:
            return False


class book1(configuration):

    def __init__(self, nop, wpp, words):

        words = sorted(words)

        super().__init__(nop, wpp, words)
        self.index = {}

        for word in words:
            self.index[word[0]] = -1

        for page in self.pages:
            for word in page:
                if self.index[word[0]] == -1:
                    self.index[word[0]] = self.pages.index(page)

    def get_index(self, word):
        return self.index[word[0]]

    def set_index(self, char, page_num):
        self.index[char] = page_num

    def test_config(self, list_senct):
        valid_senct = 0
        pg_turn = 0
        totw = 0
        c = 0
        for senct in list_senct:

            c += 1
            if self.test_senct(senct):
                valid_senct += 1
                for token in senct:
                    found = False
                    lemma = token[1]
                    totw += 1
                    currpage = self.get_index(lemma)
                    pg_turn += 1

                    while(not found):
                        if self.in_page(lemma, currpage):
                            found = True
                            break
                        currpage += 1
                        pg_turn += 1
                    pg_turn += 1

                    if currpage >= self.get_nop():
                        print('WORD NOT FOUND!\nERROR')
                        return None

        return (pg_turn / valid_senct, pg_turn / totw, valid_senct)


class book2(configuration):

    def __init__(self, nop, wpp, words):

        temp = []
        for w in words:
            temp.append(nltk.pos_tag([w])[0])

        word_temp = sorted(temp, key=itemgetter(1))
        words = list(w[0] for w in word_temp)

        super().__init__(nop, wpp, words)
        self.index = {}
        for word in words:
            tag = nltk.pos_tag([word])[0][1]
            self.index[tag] = -1

        for page in self.pages:
            for word in page:
                tag = nltk.pos_tag([word])[0][1]
                if self.index[tag] == -1:
                    self.index[tag] = self.pages.index(page)

    def get_index(self, word):
        tag = nltk.pos_tag([word])[0][1]
        return self.index[tag]

    def set_index(self, char, page_num):
        self.index[char] = page_num

    def test_config(self, list_senct):
        valid_senct = 0
        pg_turn = 0
        totw = 0
        c = 0
        for senct in list_senct:

            c += 1
            if self.test_senct(senct):
                valid_senct += 1
                for token in senct:
                    found = False
                    lemma = token[1]
                    totw += 1
                    currpage = self.get_index(lemma)
                    pg_turn += 1

                    while(not found):
                        if self.in_page(lemma, currpage):
                            found = True
                            break
                        currpage += 1
                        pg_turn += 1

                        if currpage >= self.get_nop():
                            print('WORD NOT FOUND!\nERROR')
                            return None

        return (pg_turn / valid_senct, pg_turn / totw, valid_senct)


class book3(configuration):

    def __init__(self, nop, wpp, words):

        temp = []
        for w in words:
            temp.append(nltk.pos_tag([w])[0])

        word_temp = sorted(temp, key=itemgetter(1, 0))
        words = list(w[0] for w in word_temp)
        super().__init__(nop, wpp, words)
        self.index = {}

        for word in words:
            tag = nltk.pos_tag([word])[0][1]
            self.index[(tag, word[0])] = -1

        for page in self.pages:
            for word in page:
                tag = nltk.pos_tag([word])[0][1]
                char = word[0]
                if self.index[(tag, char)] == -1:
                    self.index[(tag, char)] = self.pages.index(page
                                                               )

    def get_index(self, word):
        tag = nltk.pos_tag([word])[0][1]
        return self.index[(tag, word[0])]

    def set_index(self, char, page_num):
        self.index[char] = page_num

    def test_config(self, list_senct):
        valid_senct = 0
        pg_turn = 0
        totw = 0
        c = 0
        for senct in list_senct:

            c += 1
            if self.test_senct(senct):
                valid_senct += 1
                for token in senct:
                    found = False
                    lemma = token[1]
                    totw += 1
                    currpage = self.get_index(lemma)
                    pg_turn += 1

                    while(not found):
                        if self.in_page(lemma, currpage):
                            found = True
                            break
                        currpage += 1
                        pg_turn += 1

                        if currpage >= self.get_nop():
                            print('WORD NOT FOUND!\nERROR')
                            return None

        return (pg_turn / valid_senct, pg_turn / totw, valid_senct)


class book4(configuration):

    def __init__(self, nop, wpp, words):

        words = sorted(words)
        self.bigram_data = []

        with open(PATH + '\\data\\bigram_data.json', 'r+') as fp:
            self.bigram_data = json.load(fp)

        super().__init__(nop, wpp, words)
        self.index = {}

        for word in words:
            self.index[word[0]] = -1

        for page in self.pages:
            for word in page:
                if self.index[word[0]] == -1:
                    self.index[word[0]] = self.pages.index(page)

    def get_index(self, word):
        return self.index[word[0]]

    def set_index(self, char, page_num):
        self.index[char] = page_num

    def get_prediction(self, word):
        req_data = set()

        for token in self.bigram_data[word]:
            req_data.add(token[1])

        return req_data

    def test_config(self, list_senct):
        valid_senct = 0
        pg_turn = 0
        totw = 0
        c = 0
        prev_lemma = '$'
        for senct in list_senct:

            c += 1
            if self.test_senct(senct):
                valid_senct += 1
                for token in senct:
                    found = False
                    lemma = token[1]
                    totw += 1

                    if token == senct[0]:
                        if lemma in self.get_prediction('^'):
                            pg_turn += 1
                            prev_lemma = lemma
                            continue
                        else:
                            pg_turn += 1

                    if lemma in self.get_prediction(prev_lemma):
                        pg_turn += 1
                        prev_lemma = lemma
                        # print('FOUND1')
                        continue
                    else:
                        pg_turn += 1

                    currpage = self.get_index(lemma)
                    pg_turn += 1

                    while(not found):
                        if self.in_page(lemma, currpage):
                            found = True
                            break
                        currpage += 1
                        pg_turn += 1
                    pg_turn += 1
                    prev_lemma = lemma
                    if currpage >= self.get_nop():
                        print('WORD NOT FOUND!\nERROR')
                        return None

        return (pg_turn / valid_senct, pg_turn / totw, valid_senct)


class book5(configuration):

    def __init__(self, nop, wpp, words):

        words = sorted(words)
        self.trigram_data = dict()
        temp_data = []
        with open(PATH + '\\data\\trigram_data.json', 'r+') as fp:
            temp_data = json.load(fp)

        for item in temp_data:
            self.trigram_data[tuple(item['key'])] = item['value']

        super().__init__(nop, wpp, words)
        self.index = {}

        for word in words:
            self.index[word[0]] = -1

        for page in self.pages:
            for word in page:
                if self.index[word[0]] == -1:
                    self.index[word[0]] = self.pages.index(page)

    def get_index(self, word):
        return self.index[word[0]]

    def set_index(self, char, page_num):
        self.index[char] = page_num

    def get_prediction(self, word_a, word_b):
        req_data = set()

        for token in self.trigram_data[(word_a, word_b)]:
            req_data.add(token[1])

        return req_data

    def test_config(self, list_senct):
        valid_senct = 0
        pg_turn = 0
        totw = 0
        c = 0
        prev_lemma_a = '$'
        prev_lemma_b = '$'
        for senct in list_senct:

            c += 1
            if self.test_senct(senct):
                valid_senct += 1
                for token in senct:
                    found = False
                    lemma = token[1]
                    totw += 1

                    if token == senct[0]:
                        if lemma in self.get_prediction('^', '^'):
                            pg_turn += 1
                            prev_lemma_a = '^'
                            prev_lemma_b = lemma
                            continue
                            # print('noooo')
                        else:
                            pg_turn += 1
                    if len(senct) > 1:
                        if token == senct[1]:
                            if lemma in self.get_prediction(prev_lemma_a, prev_lemma_b):
                                prev_lemma_a = prev_lemma_b
                                prev_lemma_b = lemma
                                pg_turn += 1
                                continue
                                # print('noooo')
                            else:
                                pg_turn += 1

                    if lemma in self.get_prediction(prev_lemma_a, prev_lemma_b):
                        pg_turn += 1
                        prev_lemma_a = prev_lemma_b
                        prev_lemma_b = lemma
                        # print('found3')
                        continue
                        # print('noooo')
                    else:
                        pg_turn += 1

                    # print('notfound')
                    currpage = self.get_index(lemma)
                    pg_turn += 1

                    while(not found):
                        if self.in_page(lemma, currpage):
                            found = True
                            break
                        currpage += 1
                        pg_turn += 1
                    pg_turn += 1
                    prev_lemma_a = prev_lemma_b
                    prev_lemma_b = lemma
                    if currpage >= self.get_nop():
                        print('WORD NOT FOUND!\nERROR')
                        return None

        return (pg_turn / valid_senct, pg_turn / totw, valid_senct)
