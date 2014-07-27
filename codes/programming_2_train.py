import sys
from collections import defaultdict

counts = defaultdict(lambda: 0)
context_counts = defaultdict(lambda: 0)

total_count = 0

with open(sys.argv[1], "r") as input_file:
   for line in input_file.readlines():
      line = line.split()
      line.insert(0, '<s>')
      line.append('</s>')
      for word_prev, word in zip(line[:-1], line[1:]):
         counts[word_prev +' '+ word] += 1
         context_counts[word_prev] += 1
         counts[word] += 1
         context_counts[""] += 1

for k,v in sorted(counts.items()):
   words = k.split(' ')
   words.pop()
   context = "".join(words)
   probability = v / float(context_counts[context])
   print "%s  %f" %(k, probability)

# test with "python programming_2_train.py ../test/02-train-input.txt >> 02-train.model"
