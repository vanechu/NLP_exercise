import sys
from math import log

count_dict = {}
with open(sys.argv[1], "r") as model:
   for line in model.readlines():
      count_dict[line.split()[0]] = float(line.split()[1])

lam = 0.95
lam_unk = 1 - lam
V = 1000000
W = 0
H = 0
unk = 0

with open(sys.argv[2], "r") as test_file:
   for line in test_file.readlines():
      line = line.split()
      line.append('</s>')
      for word in line:
         W += 1
         P = float(lam_unk) / V
         if word in count_dict:
            P += lam * count_dict[word]
         else:
            unk += 1
         H += -log(P, 2)

print H / W
print float(W - unk) / W

# test with "python programming_1_test.py 01-train.model ../test/01-test-input.txt"
