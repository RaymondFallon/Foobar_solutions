##  The following was a challenge problem from Google:
##
##  Running with Bunnies
##  ====================
##
##  You and your rescued bunny prisoners need to get out of this collapsing
##  death trap of a space station - and fast! Unfortunately, some of the
##  bunnies have been weakened by their long imprisonment and can't run
##  very fast. Their friends are trying to help them, but this escape
##  would go a lot faster if you also pitched in. The defensive bulkhead
##  doors have begun to close, and if you don't make it through in time,
##  you'll be trapped! You need to grab as many bunnies as you can and
##  get through the bulkheads before they close. 
##
##  The time it takes to move from your starting point to all of the
##  bunnies and to the bulkhead will be given to you in a square
##  matrix of integers. Each row will tell you the time it takes to
##  get to the start, first bunny, second bunny, ..., last bunny, and
##  the bulkhead in that order. The order of the rows follows the same
##  pattern (start, each bunny, bulkhead). The bunnies can jump into
##  your arms, so picking them up is instantaneous, and arriving at
##  the bulkhead at the same time as it seals still allows for a
##  successful, if dramatic, escape. (Don't worry, any bunnies you
##  don't pick up will be able to escape with you since they no longer
##  have to carry the ones you did pick up.) You can revisit different
##  spots if you wish, and moving to the bulkhead doesn't mean you have
##  to immediately leave - you can move to and from the bulkhead to pick
##  up additional bunnies if time permits.
##
##  In addition to spending time traveling between bunnies, some paths
##  interact with the space station's security checkpoints and add time
##  back to the clock. Adding time to the clock will delay the closing
##  of the bulkhead doors, and if the time goes back up to 0 or a positive
##  number after the doors have already closed, it triggers the bulkhead
##  to reopen. Therefore, it might be possible to walk in a circle and
##  keep gaining time: that is, each time a path is traversed, the same
##  amount of time is used or added.
##
##  Write a function of the form answer(times, time_limit) to calculate
##  the most bunnies you can pick up and which bunnies they are, while
##  still escaping through the bulkhead before the doors close for good.
##  If there are multiple sets of bunnies of the same size, return the
##  set of bunnies with the lowest prisoner IDs (as indexes) in sorted
##  order. The bunnies are represented as a sorted list by prisoner ID,
##  with the first bunny being 0. There are at most 5 bunnies, and
##  time_limit is a non-negative integer that is at most 999.
##
##  For instance, in the case of
##  [
##    [0, 2, 2, 2, -1],  # 0 = Start
##    [9, 0, 2, 2, -1],  # 1 = Bunny 0
##    [9, 3, 0, 2, -1],  # 2 = Bunny 1
##    [9, 3, 2, 0, -1],  # 3 = Bunny 2
##    [9, 3, 2, 2,  0],  # 4 = Bulkhead
##  ]
##  and a time limit of 1, the five inner array rows designate the
##  starting point, bunny 0, bunny 1, bunny 2, and the bulkhead door
##  exit respectively. You could take the path:
##
##  Start End Delta Time Status
##      -   0     -    1 Bulkhead initially open
##      0   4    -1    2
##      4   2     2    0
##      2   4    -1    1
##      4   3     2   -1 Bulkhead closes
##      3   4    -1    0 Bulkhead reopens; you and the bunnies exit
##
##  With this solution, you would pick up bunnies 1 and 2. This is the best
##  combination for this space station hallway, so the answer is [1, 2].

##  Here is my solution:

import copy
import queue

def answer(times, time_limit):
  """
  We conduct our search in three parts:
  One: Run Bellman-Ford to hunt for any negative cycles
  Two: Run Floyd-Warshall to find the min-path between all pairs of locations
  Three: Search through each worthwhile path until we find the path that saves
         the maximum amount of bunnies
  """

  # First we run a basic Bellman-Ford algo to search for negative weight cycles
  
  shortest_p = copy.deepcopy(times[0])  # fastest time from start to each node 

  def relax(node, neighbor):
    if shortest_p[node] > shortest_p[neighbor] + times[neighbor][node]:
      shortest_p[node] = shortest_p[neighbor] + times[neighbor][node]
    
  for i in range(len(times) - 1):
    for u in range(len(times)):
      for v in range(len(times)):
        relax(u, v)

  for u in range(len(times)):
    for v in range(len(times)):
      if shortest_p[u] > shortest_p[v] + times[v][u]:
        # We have a negative weight cycle, so we can collect every bunny
        ans = []
        for i in range(len(times) - 2):
          ans.append(i)
        return ans
      

  # From this point onward, we can assume that we have NO negative weight cycles
  # Hey, that means we can run that sweet, sweet Floyd-Warshall algo, which will tell
  # us the shortest path between all pairs of vertices.  If going directly from
  # some node u to some node v is slower than some other path, we'll never need
  # to consider paths that step from u to v directly. With only 7 nodes, we can
  # handle that O(n**3) performance hit

  D_to_k_minus_one = copy.deepcopy(times)
  D_to_k = None
  for k in range(len(times)):
    D_to_k = copy.deepcopy(times) # we want an nxn matrix, all entries will be replaced
    for i in range(len(times)):
      for j in range(len(times)):
        D_to_k[i][j] = min([D_to_k_minus_one[i][j],
                            D_to_k_minus_one[i][k] + D_to_k_minus_one[k][j]])
    D_to_k_minus_one = copy.deepcopy(D_to_k)

  # First, we make note of the shortest path out to the bulkhead
  # This will help use pare down our worthwhile potential solutions later
  shortest_p_to_bulkhead = [D_to_k[i][len(times) - 1] for i in range(len(times))]

  # Now D_to_k[i][j] will be a 1 if a direct path from i to j is the shortest path
  # and will be a 0 otherwise
  for i in range(len(times)):
    for j in range(len(times)):
      if D_to_k[i][j] < times[i][j]:
        D_to_k[i][j] = 0
      else:
        D_to_k[i][j] = 1

  
        
  class Path():
    """
    This class will help us quickly spawn new paths in our search queue
    """
      
    def __init__(self, prev_path, new_node):
      if prev_path != None:
        self.path = copy.copy(prev_path.path)
        self.path.append(new_node)
        self.time_elapsed = prev_path.time_elapsed + times[prev_path.path[-1]][new_node]
      else: # only used for very first Path call
        self.path = [0]
        self.time_elapsed = 0
        
    def waste_cycle(self):
      # Are we going in any cycles that contain no new prisoner-nodes?
      # (Such a cycle would never be helpful with no negative cycles)
      # Returns True if Path IS a waste cycle and shouldn't be considered
      last_node = self.path[-1]
      if last_node in self.path[:-1]:
        current_cycle = [last_node]
        node = None
        counter = 2
        while True:
          node = self.path[-1 * counter]
          counter += 1
          current_cycle.append(node)
          if node == last_node:
            break
        prev_visited = set(self.path[:-1 * (counter - 2)])
        old_nodes = 0        
        for n in current_cycle:
          if n == len(times) - 1:
            old_nodes += 1
          elif n in prev_visited:
            old_nodes += 1
        if old_nodes == len(current_cycle):
          return True
      else:
        return False
            
        
      
    def good_to_go(self):
      # A list of deal-breakers for adding our path to queue:

      last_node = self.path[-1]
      
      # Will this path take longer than we have, even utilizing potential neg weights?
      if self.time_elapsed > time_limit - shortest_p_to_bulkhead[last_node]:
        return False
      # Are we going from u->v directly when indirectly would be faster?
      if D_to_k[self.path[-2]][last_node] == 0:
        return False
      # Are we going in any cycles that contain no new prisoner-nodes?
      if self.waste_cycle():
        return False

      # This Path is "Good To Go" into the queue
      return True

  def better_than_best(new_p, best):
    if new_p.time_elapsed <= time_limit:
      if new_p.path[-1] == len(times) - 1:
        if len(set(new_p.path)) > len(set(best.path)):
          return True
    else:
      return False
    
  # Now we can start our queue from the starting point
  
  best = Path(None, 0)
  search_queue = queue.Queue()
  search_queue.put(best)
  while(not search_queue.empty()):
    old_path = search_queue.get()
    last_node = old_path.path[-1]
    # Consider going in every direction from the end of the popped path
    for i in range(len(times)): 
      if i != last_node: # Don't stay in same area
        new_path = Path(old_path, i)
        if new_path.good_to_go():
          search_queue.put(new_path)
          if better_than_best(new_path, best):
            best = new_path
            # If we have found a path that collects all bunnies, stop looking!
            if len(set(best.path)) == len(times):
              ans = []
              for i in set(best.path):
                if 0 < i < len(times) - 1:
                  ans.append(i - 1)
              ans.sort()
              return ans
            
  ans = []
  for i in set(best.path):
    if 0 < i < len(times) - 1:
      ans.append(i - 1)
  ans.sort()
      
  return ans


