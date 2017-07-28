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


