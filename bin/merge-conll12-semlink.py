from __future__ import print_function


conll12_fname = "/home/strubell/research/data/conll-2012-new/conll2012-train.txt"
semlink_fname = "/home/strubell/research/data/semlink-1.2.2c/semlink-wsj.txt"

remove_list = ['rel', 'LINK-SLC']

semlink_map = {}
with open(semlink_fname, 'r') as semlink_file:
  for line in semlink_file:
    line = line.strip()
    if line:
      split_line = line.split()

      # key is doc name without ending + sentence number
      key = (split_line[0].split('.')[0], split_line[1])

      # value is predicate + args
      args = split_line[10:]
      # take just the verbnet senses
      stripped_args = map(lambda a: '-'.join(a.split('*')[-1].split('-')[1:]).split(';')[0], args)
      stripped_removed_args = [a for a in stripped_args if a not in remove_list]
      value = (split_line[7].split('.')[0], ' '.join(stripped_removed_args))
      if key not in semlink_map:
        semlink_map[key] = []
      semlink_map[key].append(value)
print(semlink_map)

with open(conll12_fname, 'r') as conll12_file:
  # want to scan conll12 file until we find a sentence that is in semlink,
  # then process that sentence
  for line in conll12_file:
    line = line.strip()
    if line:
      split_line = line.split()
