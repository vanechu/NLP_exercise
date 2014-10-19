import sys
from collections import defaultdict
from math import log
import pprint


class HMM(object):
   def __init__(self):
      self.trans_prob = defaultdict(lambda:0)
      self.emiss_prob = defaultdict(lambda:0)
      self.tags = set([])
      self.words = set([])

   def train(self, corpus):
      emiss = defaultdict(lambda:0)
      trans = defaultdict(lambda:0)
      context = defaultdict(lambda:0) # both for the previous and current tag
      with open(corpus, "r") as f:
         for line in f.readlines():
            previous = '<s>'
            for word_tag in line.strip().split(' '):
               [word, tag] = word_tag.split('_')
               self.words.add(word)
               self.tags.add(tag)
               trans[previous + ' ' + tag] += 1
               emiss[tag + ' ' + word] += 1
               context[previous] += 1 
               previous = tag
            context[tag] += 1   # for the last word /<s>
            trans[tag + ' ' + '/<s>'] += 1
      for transition, count in trans.items():
         self.trans_prob[transition] = str(float(count) / context[transition.split(" ")[0]]) # no smothing
      for emission, count in emiss.items():
         self.emiss_prob[emission] = str(float(count) / context[emission.split(" ")[0]])
      pprint.pprint(self.emiss_prob)
      pprint.pprint(self.trans_prob)

   def load_model(self, model):
      with open(model, "r") as f:
         for line in f.readlines():
            T_or_E = line.strip().split(" ")[0]
            prev = line.strip().split(" ")[1]
            next = line.strip().split(" ")[2] # tag or word included
            prob = line.strip().split(" ")[3]
            pair_tag = " ".join(line.split(" ")[1:3])

            if T_or_E == 'T':   
               self.trans_prob[pair_tag] = prob
               self.tags.add(prev)
               self.tags.add(next)
            elif T_or_E == 'E':
               self.emiss_prob[pair_tag] = prob
               self.words.add(next)
      print "load:"
      pprint.pprint(self.emiss_prob)
      pprint.pprint(self.trans_prob)
      # print self.tags
      # print self.words

   def smooth(self):
      para_lambda = 0.95
      N = len(self.words)

      for tag in self.tags:
         for word in self.words:
            pair = tag + " " + word
            if pair in self.emiss_prob:
               self.emiss_prob[pair] = para_lambda * float(self.emiss_prob[pair]) + (1 - para_lambda) * (1.0 / N)
            else:
               self.emiss_prob[pair] = (1 - para_lambda) * (1.0 / N)
      # pprint.pprint(self.emiss_prob)

   def forward_backward(self, input_file):
      with open(input_file, 'r') as f:
         for line in f.readlines():
            best_score = {}
            best_edge = {}
            best_score["0 <s>"]  = 0
            length = len(line.strip().split())
            for i in xrange(length):
               for prev in self.tags:
                  for next in self.tags:
                     status_pair = str(i) + " " + prev
                     next_status_pair = str(i+1) + " " + next
                     trans_pair = prev + " " + next
                     emiss_pair = next + " " + line.strip().split()[i]
                     if status_pair in best_score and trans_pair in self.trans_prob:
                        score = best_score[status_pair] + -log(float(self.trans_prob[trans_pair])) + -log(float(self.emiss_prob[emiss_pair])) 
                        if next_status_pair not in best_score or best_score[next_status_pair] > score:
                           best_score[next_status_pair] = score
                           best_edge[next_status_pair] = str(i) + " " + prev

            for prev in self.tags:  # for '</s>'
               status_pair = str(length) + " " + prev
               trans_pair = prev + " " + "</s>"
               next_status_pair = str(length+1) + " " + next
               if status_pair in best_score and trans_pair in self.trans_prob:
                  score = best_score[status_pair] + -log(float(self.trans_prob[trans_pair]))
                  if next_status_pair not in best_score or best_score[next_status_pair] > score:
                     best_score[next_status_pair] = score
                     best_edge[next_status_pair] = str(length) + " " + prev

            tags = []
            next_edge = best_edge[str(length+1) + " </s>"]
            while next_edge != "0 <s>":
               position, tag = next_edge.split()
               tags.append(tag)
               next_edge = best_edge[next_edge]
            tags.reverse()
            print " ".join(tags)

# with open(sys.argv[1], "r") as input_file:
#    unigram = load_model(input_file)


# with open(sys.argv[2], "r") as input_file:
#    forward_backward(input_file)

if __name__ == "__main__":
   hmm = HMM()
   # hmm.train("../test/05-train-input.txt")
   hmm.load_model("../test/05-train-answer.txt")
   hmm.smooth()
   hmm.forward_backward("../test/05-test-input.txt")
