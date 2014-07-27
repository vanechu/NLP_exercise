import sys
from math import log

probability = {}
with open(sys.argv[1], "r") as model:
   for line in model.readlines():
      probability[line.split("  ")[0]] = float(line.split("  ")[1])

lam1 = 0.95
lam1_unk = 1 - lam1
lam2 = 0.9
lam2_unk = 1 - lam2
V = 1000000
W = 0
H = 0

with open(sys.argv[2], "r") as test_file:
   for line in test_file.readlines():
      line = line.split()
      line.append('</s>')
      line.insert(0, '<s>')
      for word_prev, word in zip(line[:-1], line[1:]):
         P1 = lam1 * probability[word] + lam1_unk / V
         P2 = lam2 * probability[word_prev +' '+ word] + lam2_unk * P1
         H += -log(P2, 2)
         W += 1

print H / W

# test with "python programming_2_test.py 02-train.model ../test/02-train-input.txt"
