import sys
from collections import defaultdict

count_dict = defaultdict(lambda: 0)

total_count = 0

with open(sys.argv[1], "r") as input_file:
   for line in input_file.readlines():
      line = line.split()
      line.append('</s>')
      for word in line:
         count_dict[word] += 1
         total_count +=1

for k,v in sorted(count_dict.items()):
   print "%s %r" %(k, float(v) / total_count)

# test with "python programming_1_train.py ../test/01-train-input.txt"
