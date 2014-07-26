import sys
from collections import defaultdict

def creat_features(words):
   phi = defaultdict(lambda: 0)
   for word in words:
      phi[word] += 1
   return phi

def predict_one(phi, weights):
   score = 0.0
   for word,count in phi.items():
      score += weights[word] * count
   if score >= 0:
      return 1
   return -1

def predict_all():
   weights = defaultdict(lambda:0.0)
   with open(sys.argv[1], "r") as model:
      for line in model.readlines():
         weights[line.split()[0]] = float(line.split()[1])

   with open(sys.argv[2], "r") as data:
      for line in data.readlines():
         words = line.split()[1:]
         phi = creat_features(words)
         y_pred = predict_one(weights, phi)
         print y_pred

predict_all()

# test with "python programming_3_test.py 03-train.model ../test/03-train-input.txt"
