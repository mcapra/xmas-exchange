import random
import datetime

today = datetime.date.today()
year = today.year

MAX_YEAR_LOOKBACK = 2
MATCHES_DIR = 'matches'
# list of people giving/receiving gifts
people = ['Matt', 'Mary', 'Phil', 'Nate', 'Dan', 'Bre']

# disallowed matches -- person p cannot give to anyone in bad_matches[p]
bad_matches = dict()
for person in people:
  bad_matches[person] = []

# get previous MAX_YEAR_LOOKBACK matches, add to bad_matches dict
def gen_bad_matches():
  for i in range(0,MAX_YEAR_LOOKBACK):
    check_year = year - (i+1)
    filename = f'{MATCHES_DIR}/{check_year}.md'
    print(filename)
    file1 = open(filename, 'r')

    Lines = file1.readlines()
    
    # Strips the newline character
    for line in Lines[2:]:
        names = line.rstrip()[1:-1].split("|") # remove newlines, remove preceding | and trailing |, split to list
        bad_matches[names[0]].append(names[1])

# sort people so that those with disallowed matches appear first and therefore
# have a greater chance of finding a valid match in the possible remaining
# receivers
people.sort(key=lambda p: 0 if p not in bad_matches else len(bad_matches[p]),
            reverse=True)

# helper function to check if giver can give to receiver
def can_match(giver, receiver):
  return giver != receiver and (giver not in bad_matches or
                                  receiver not in bad_matches[giver])

# keep trying to generate all matches, stopping if it takes too many iterations
gen_bad_matches()
matches = {}
iters = 0
while iters < 10 and len(matches) < len(people):
  iters += 1
  # create a list of all possible receivers from people, copying to allow for
  # mutation later
  receivers = [p for p in people]
  # find a receiver for each giver
  for giver in people:
    # generate a list of possible receiver for this giver
    valid_receivers = [r for r in receivers if can_match(giver, r)]
    # start over if there are no valid receivers left for this giver
    if len(valid_receivers) == 0:
        break
    # pick a random valid receiver
    receiver = random.choice(valid_receivers)
    matches[giver] = receiver
    # remove the chosen receiver so that each person only receives one gift
    receivers.remove(receiver)

# fail if not able to generate all matches
if len(matches) < len(people):
  print(f'Could not generate valid matches in {iters} iteration(s).')
  exit(1)

# print all matches, with nice formatting
print(f'Valid matches generated in {iters} iteration(s):')
max_giver_len = max([len(p) for p in people])
for giver in matches:
  # pad giver with spaces so all arrows line up
  print(giver + ' ' * (max_giver_len - len(giver)) + ' -> ' + matches[giver])