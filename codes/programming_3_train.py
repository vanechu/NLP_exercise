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

def update_weights(weights, phi, label):
   for word, value in phi.items():
      weights[word] += value * label

def learning(weights, data):
   for line in data.readlines():
      label = int(line.split()[0])
      words = line.split()[1:]
      # print "label",words
      phi = creat_features(words)
      label_pred = predict_one(phi, weights)
      if label != label_pred:
         update_weights(weights, phi, label)

with open(sys.argv[1], "r") as input_file:
   weights = defaultdict(lambda:0.0)
   learning(weights, input_file)
   for k,v in weights.items():
      print "%s %f"  % (k, v)

# test with "python programming_3_train.py ../test/03-train-input.txt >> 03-train.model"
