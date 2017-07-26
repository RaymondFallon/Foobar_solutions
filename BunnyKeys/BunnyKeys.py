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
