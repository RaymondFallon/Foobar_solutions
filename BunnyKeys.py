##  The following was a challenge problem from Google:
##
##  Free the Bunny Prisoners
##  ========================
##
##  You need to free the bunny prisoners before Commander Lambda's space station explodes!
##  Unfortunately, the commander was very careful with her highest-value prisoners -
##  they're all held in separate, maximum-security cells. The cells are opened by
##  putting keys into each console, then pressing the open button on each console
##  simultaneously. When the open button is pressed, each key opens its corresponding
##  lock on the cell. So, the union of the keys in all of the consoles must be all of
##  the keys. The scheme may require multiple copies of one key given to different minions.
##
##  The consoles are far enough apart that a separate minion is needed for each one.
##  Fortunately, you have already freed some bunnies to aid you - and even better, you were
##  able to steal the keys while you were working as Commander Lambda's assistant. The
##  problem is, you don't know which keys to use at which consoles. The consoles are
##  programmed to know which keys each minion had, to prevent someone from just stealing
##  all of the keys and using them blindly. There are signs by the consoles saying how many
##  minions had some keys for the set of consoles. You suspect that Commander Lambda has a
##  systematic way to decide which keys to give to each minion such that they could use
##  the consoles.
##
##  You need to figure out the scheme that Commander Lambda used to distribute the keys.
##  You know how many minions had keys, and how many consoles are by each cell.  You know
##  that Command Lambda wouldn't issue more keys than necessary (beyond what the key
##  distribution scheme requires), and that you need as many bunnies with keys as there
##  are consoles to open the cell.
##
##  Given the number of bunnies available and the number of locks required to open a cell,
##  write a function answer(num_buns, num_required) which returns a specification of how
##  to distribute the keys such that any num_required bunnies can open the locks, but no
##  group of (num_required - 1) bunnies can.
##
##  Each lock is numbered starting from 0. The keys are numbered the same as the lock they
##  open (so for a duplicate key, the number will repeat, since it opens the same lock).
##  For a given bunny, the keys they get is represented as a sorted list of the numbers
##  for the keys. To cover all of the bunnies, the final answer is represented by a sorted
##  list of each individual bunny's list of keys.  Find the lexicographically least such
##  key distribution - that is, the first bunny should have keys sequentially starting
##  from 0.
##
##  num_buns will always be between 1 and 9, and num_required will always be between
##  0 and 9 (both inclusive).  For example, if you had 3 bunnies and required only 1 of
##  them to open the cell, you would give each bunny the same key such that any of the 3
##  of them would be able to open it, like so:
##   [[0],
##    [0],
##    [0]]
##  If you had 2 bunnies and required both of them to open the cell, they would receive
##  different keys (otherwise they wouldn't both actually be required), and your answer
##  would be as follows:
##   [[0],
##    [1],]
##  Finally, if you had 3 bunnies and required 2 of them to open the cell, then any 2 of
##                  the 3 bunnies should have all of the keys necessary to open the cell,
##                  but no single bunny would be able to do it.  Thus, the answer would be:
##   [[0, 1],
##    [0, 2],
##    [1, 2],]

## Here is my solution:

def answer(num_buns, num_required):
  """
  We find the answer by constructing a num_buns by num_keys matrix,
  called columns, in which columns[b][k] == 1 if bunny b has key k
  and 0 otherwise
  """
  if num_required == 0:
    ans = []
    for b in range(num_buns):
      ans.append([])
    return ans

  def make_next_column(binary_counter):
    # takes the binary_counter and increments until it has exactly
    # zeroes_per_column number of 1's in it. Once it does, it returns the
    # next column, which is essential ~binary_counter
    column = []
    for i in range(num_buns):
      column.append(1)
    while(True):
      bin_c = bin(binary_counter)
      bin_c = str(bin_c)
      bin_c = [int(i) for i in bin_c[2:]]
      if sum(bin_c) == zeroes_per_column:
        for i in range(1, len(bin_c) + 1, 1):
          if bin_c[-1 * i] == 1:
            column[-1 * i] = 0
        return column, binary_counter      
      else:
        binary_counter += 1
  
  extr_buns = num_buns - num_required # extraneous bunnies
  ones_per_column = extr_buns + 1
  zeroes_per_column = num_buns - ones_per_column
  columns = []
  binary_counter = 2**zeroes_per_column - 2
  endpoint = 0
  for i in range(zeroes_per_column):
    endpoint += 2**(num_buns - i - 1)
  while binary_counter < endpoint:
    binary_counter += 1
    column, binary_counter = make_next_column(binary_counter)
    columns.append(column)
  num_keys = len(columns)
  ans = []
  for b in range(num_buns):
    ans.append([])
    for k in range(num_keys):
      if columns[k][b] == 1:
        ans[b].append(k)
      
  return ans
