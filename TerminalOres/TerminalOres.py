import queue
import copy
from fractions import gcd, Fraction

def answer(m):

  path_probs = {(0): Fraction(1, 1)}
  ## Takes the trace of a finished path to 
  def concat_with_prob(trace):
    prev_path, last_state = tuple(trace[:-1]), trace[-1] # split the path into 2 parts
    if prev_path in path_probs:
      my_prob = path_probs[prev_path]
      my_prob *= Fraction(m[prev_path[-1]][last_state], sum(m[prev_path[-1]]))
    else:
      my_prob = Fraction(1, 1)
      for i in range(len(trace) - 1):
        my_prob *= Fraction(m[trace[i]][trace[i+1]], sum(m[trace[i]]))
    path_probs[tuple(trace)] = my_prob
  
  def lcm(x, y):
    """This function takes two integers and returns the L.C.M.
    This fuction stolen mercilessly from:
    https://www.programiz.com/python-programming/examples/lcm"""

    # choose the greater number
    if x > y:
      greater = x
    else:
      greater = y

    while(True):
      if ((greater % x == 0) and (greater % y == 0)):
        lcm = greater
        break
      greater += 1

    return lcm

  num_states = len(m)
  the_term_states = []
  the_unstable_states = []
  paths_to_stability = [] 
  blank_array = []
  for i in range(num_states):
    blank_array.append(0)
  for i in range(num_states):
    if m[i] == blank_array:
      the_term_states.append(i) # Collect the terminal states
    else:
      the_unstable_states.append(i) # Collect the unstable states
  search_queue = queue.Queue()
  search_queue.put([0])

  ## Find every possible (non-repeating) path from s0 to a terminal state
  while not search_queue.empty(): 
    trace = search_queue.get()
    state = trace[-1]
    for x in range(num_states):
      if m[state][x] != 0:
        if x in the_term_states:
          new_trace = copy.deepcopy(trace)
          new_trace.append(x)
          concat_with_prob(new_trace)
          paths_to_stability.append(new_trace)
        else:
          if x not in trace:
            new_trace = copy.deepcopy(trace)
            new_trace.append(x)
            search_queue.put(new_trace)

  ## term_state_probs will hold the probabilites for each terminal state that
  ## the ore will end in this state without every having repeated an unstable state
  ## (ie: the sum of all these probabilities may be less than 1)
  term_state_probs = {}  
  for s in the_term_states:
    term_state_probs[s] = Fraction(0, 1)
  for path in paths_to_stability:
    final_state = path[-1]
    term_state_probs[final_state] += path_probs[tuple(path)]
  total_prob = Fraction(0, 1)
  my_lcm = 0
  for s in the_term_states:
    total_prob += term_state_probs[s]
    if my_lcm == 0:
      my_lcm = term_state_probs[s].denominator
    else:
      my_lcm = lcm(my_lcm, term_state_probs[s].denominator)
  ans = []
  for s in the_term_states:
    my_prob = term_state_probs[s]
    num = (my_lcm // my_prob.denominator)
    num *= my_prob.numerator
    ans.append(num)
  ans.append(sum(ans))
  return ans
