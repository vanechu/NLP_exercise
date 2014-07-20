import sys
from collections import defaultdict

count_dict = defaultdict(lambda: 0)

with open(sys.argv[1], "r") as input_file:
   for line in input_file.readlines():
      for word in line.split():
         count_dict[word] += 1

for k,v in count_dict.items():
   print "%s %r" %(k,v)

# test with "python programming_1.py ../test/00-input.txt"
