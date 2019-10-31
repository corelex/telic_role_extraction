import collections
import queue
from nltk import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.parse import CoreNLPParser
from nltk.parse.corenlp import CoreNLPDependencyParser


class KitchenTools():
    def __init__(self, tool, file):

        self.t_name = tool
        self.t_synset = wn.synset(self.t_name)
        self.hypernyms = []
        self.level = 0

        self.file = file

        self.parser = CoreNLPParser(url='http://localhost:9000')
        self.dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')

        self.telic_roles = []
        self.first_words = []

    def parse_def(self):

        definition = self.t_synset.definition()
        self.file.write(self.t_name + ': ')
        self.file.write(definition + '\n')
        parses = self.dep_parser.parse(word_tokenize(definition))
        deps = [[(gov, rel, dep) for gov, rel, dep in parse.triples()] for parse in parses]
        deps = deps[0]

        for d in deps:
            self.file.write(str(d) + '\n')

        self.find_first_words(deps)
        if len(self.first_words) != 0:
            for first_word in self.first_words:
                self.telic_roles.extend(self.recursive_depth_search(deps, first_word))
        kich_tool.file.write(' '.join(self.telic_roles) + '\n')

        self.file.write('\n')

    def find_first_words(self, deps):
        '''for d in deps:
            if d[2][0] == 'for' and (d[1] == 'mark' or d[1] == 'case'):
                self.first_words.append(d[0][0])
        if len(self.first_words) == 0:'''
        for d in deps:
            if d[0][0] == 'used' and (d[1] == 'xcomp' or d[1] == 'advcl' or d[1] == 'nmod'):
                self.first_words.append(d[2][0])

    def recursive_depth_search(self, deps, next_word):
        put_in_front = ['case', 'det', 'mark', 'amod', 'compound']
        left_que = queue.Queue()
        right_que = queue.Queue()
        left_str = list()
        right_str = list()
        for dep in deps:
            if dep[0][0] == next_word:
                if dep[1] in put_in_front:
                    left_que.put(dep[2][0])
                else:
                    right_que.put(dep[2][0])
        while left_que.empty() is False:
            d = left_que.get()
            left_part = self.recursive_depth_search(deps, d)
            if left_part is not None:
                left_str.extend(left_part)
        while right_que.empty() is False:
            d = right_que.get()
            right_part = self.recursive_depth_search(deps, d)
            if right_part is not None:
                right_str.extend(right_part)
        left_str.append(next_word)
        if len(right_str) != 0:
            left_str.extend(right_str)
        return left_str


if __name__ == '__main__':
    kitchen_tools = ['spoon.n.01', 'table_knife.n.01', 'fork.n.01', 'chopstick.n.01', 'pan.n.01', 'plate.n.04', 'pot.n.01', 'bowl.n.01', 'grid.n.05', 'griddle.n.01', 'skimmer.n.02', 'steamer.n.02', 'turner.n.08']
    kitchen_utensil = [s.name() for s in wn.synset('kitchen_utensil.n.01').hyponyms()]
    kitchen_utensil_hypo1 = [h.name() for s in kitchen_utensil for h in wn.synset(s).hyponyms()]
    kitchen_utensil_hypo2 = [h.name() for s in kitchen_utensil_hypo1 for h in wn.synset(s).hyponyms()]
    kitchen_utensil_hypo3 = [h.name() for s in kitchen_utensil_hypo2 for h in wn.synset(s).hyponyms()]
    kitchen_utensil_hypo4 = [h.name() for s in kitchen_utensil_hypo3 for h in wn.synset(s).hyponyms()]
    tableware = [s.name() for s in wn.synset('tableware.n.01').hyponyms()]
    tableware_hypo1 = [h.name() for s in tableware for h in wn.synset(s).hyponyms()]
    tableware_hypo2 = [h.name() for s in tableware_hypo1 for h in wn.synset(s).hyponyms()]
    tableware_hypo3 = [h.name() for s in tableware_hypo2 for h in wn.synset(s).hyponyms()]
    tableware_hypo4 = [h.name() for s in tableware_hypo3 for h in wn.synset(s).hyponyms()]
    writing_implement = [s.name() for s in wn.synset('writing_implement.n.01').hyponyms()]
    writing_implement_hypo1 = [h.name() for s in writing_implement for h in wn.synset(s).hyponyms()]
    writing_implement_hypo2 = [h.name() for s in writing_implement_hypo1 for h in wn.synset(s).hyponyms()]
    cleaning_implement = [s.name() for s in wn.synset('cleaning_implement.n.01').hyponyms()]
    cleaning_implement_hypo1 = [h.name() for s in cleaning_implement for h in wn.synset(s).hyponyms()]
    cleaning_implement_hypo2 = [h.name() for s in cleaning_implement_hypo1 for h in wn.synset(s).hyponyms()]
    f = open('writing_implement1.txt', 'w')
    for t in writing_implement:
        kich_tool = KitchenTools(t, f)
        kich_tool.parse_def()
    f.close()

    ns = wn.all_synsets(pos='n')
    total = 0
    count = 0
    for n in ns:
        total += 1
        n_kt = KitchenTools(n.name())
        n_kt.parse_def()
        if len(n_kt.first_words) != 0:
            count += 1
    print(total)
    print(count)
