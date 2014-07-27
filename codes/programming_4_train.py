import sys
from collections import defaultdict
from math import log

def load_model(model):
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

with open(sys.argv[1], "r") as input_file:
   unigram = load_model(input_file)

with open(sys.argv[2], "r") as input_file:
   forward_backward(input_file)

# test with "python programming_4_train.py ../test/04-model.txt ../test/04-input.txt"
