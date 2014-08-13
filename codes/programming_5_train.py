import sys
from collections import defaultdict
from math import log
import pprint


class HMM(object):
   def __init__(self):
      self.trans_prob = defaultdict(lambda:0)
      self.emiss_prob = defaultdict(lambda:0)

   def train(self, corpus):
      emiss = defaultdict(lambda:0)
      trans = defaultdict(lambda:0)
      context = defaultdict(lambda:0) # both for the previous and current tag
      with open(corpus, "r") as f:
         for line in f.readlines():
            previous = '<s>'
            for word_tag in line.strip().split(' '):
               [word, tag] = word_tag.split('_')
               trans[previous + ' ' + tag] += 1
               emiss[tag + ' ' + word] += 1
               context[previous] += 1 
               previous = tag
            context[tag] += 1   # for the last word /<s>
            trans[tag + ' ' + '/<s>'] += 1
      for transition, count in trans.items():
         self.trans_prob[transition] = float(count) / context[transition.split(" ")[0]] # no smothing
      for emission, count in emiss.items():
         self.emiss_prob[emission] = float(count) / context[emission.split(" ")[0]] 
      # pprint.pprint(self.emiss_prob)

   def load_model(self, model):
      with open(model, "r") as f:
         for line in f.readlines():
            if line.split(" ")[0] == 'T':
               self.trans_prob[" ".join(line.split(" ")[1:3])] = line.strip().split(" ")[3]
            elif line.split(" ")[0] == 'E':
               self.emiss_prob[" ".join(line.split(" ")[1:3])] = line.strip().split(" ")[3]

   def forword_backword(self):
      pass

def hmm_train(model):
   unigram = defaultdict(lambda:0)
   for line in model.readlines():
      unigram[line.split()[0]] = float(line.split()[1])
   return unigram

def forward_backward(input_file):
   INF = 10 ** 10
   lam = 0.95
   lam_unk = 1 - lam
   V = 10 ** 6
   for line in input_file.readlines():
      line = line.strip()
      ary_size = len(line) + 1
      best_edge = [None] * ary_size
      best_score = [0.0] * ary_size
      for word_end in range(1, ary_size):
         best_score[word_end] = INF
         for word_begin in range(0, word_end):
            word = line[word_begin: word_end]
            if (word in unigram) :
               prob = unigram[word] / float(V)
               prob += unigram[word] * lam_unk
               my_score = best_score[word_begin] - float(log(prob, 2))
               if my_score < best_score[word_end]:
                  best_score[word_end] = my_score
                  best_edge[word_end] = (word_begin, word_end)
      words = []
      next_edge = best_edge[len(best_edge) - 1]
      while next_edge is not None:
         word = line[next_edge[0] : next_edge[1]]
         words.append(word)
         next_edge = best_edge[next_edge[0]]
      words.reverse()
      print words
      print " ".join(words)

# with open(sys.argv[1], "r") as input_file:
#    unigram = load_model(input_file)

# with open(sys.argv[2], "r") as input_file:
#    forward_backward(input_file)

if __name__ == "__main__":
   hmm = HMM()
   # hmm.train("../test/05-train-input.txt")
   hmm.load_model("../test/05-train-answer.txt")