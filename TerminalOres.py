##  The following was a challenge problem from Google:
##
##  Doomsday Fuel
##  =============
##
##  Making fuel for the LAMBCHOP's reactor core is a tricky process because of the
##  exotic matter involved. It starts as raw ore, then during processing, begins
##  randomly changing between forms, eventually reaching a stable form. There may
##  be multiple stable forms that a sample could ultimately reach, not all of which
##  are useful as fuel. 
##
##  Commander Lambda has tasked you to help the scientists increase fuel creation
##  efficiency by predicting the end state of a given ore sample. You have carefully
##  studied the different structures that the ore can take and which transitions it
##  undergoes. It appears that, while random, the probability of each structure
##  transforming is fixed. That is, each time the ore is in 1 state, it has the same
##  probabilities of entering the next state (which might be the same state).  You
##  have recorded the observed transitions in a matrix. The others in the lab have
##  hypothesized more exotic forms that the ore can become, but you haven't seen
##  all of them.
##
##  Write a function answer(m) that takes an array of array of nonnegative ints
##  representing how many times that state has gone to the next state and return
##  an array of ints for each terminal state giving the exact probabilities of each
##  terminal state, represented as the numerator for each state, then the denominator
##  for all of them at the end and in simplest form. The matrix is at most 10 by 10.
##  It is guaranteed that no matter which state the ore is in, there is a path from
##  that state to a terminal state. That is, the processing will always eventually end
##  in a stable state. The ore starts in state 0. The denominator will fit within a
##  signed 32-bit integer during the calculation, as long as the fraction is
##  simplified regularly. 
##
##  For example, consider the matrix m:
##  [
##    [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
##    [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
##    [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
##    [0,0,0,0,0,0],  # s3 is terminal
##    [0,0,0,0,0,0],  # s4 is terminal
##    [0,0,0,0,0,0],  # s5 is terminal
##  ]
##  So, we can consider different paths to terminal states, such as:
##  s0 -> s1 -> s3
##  s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
##  s0 -> s1 -> s0 -> s5
##  Tracing the probabilities of each, we find that
##  s2 has probability 0
##  s3 has probability 3/14
##  s4 has probability 1/7
##  s5 has probability 9/14
##  So, putting that together, and making a common denominator,
##  gives an answer in the form of:
##  [s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is:
##  [0, 3, 2, 9, 14].

## Here is my solution:

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
