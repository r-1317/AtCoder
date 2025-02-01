import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def serch_dst(n, a_list):
  ic(3**(n-1), type(3**(n-1)))
  next_a_list = [False]*(3**(n-1))
  for i in range(3**(n-1)):
    x = 0
    for j in range(3):
      x += a_list[i*3+j]
    if 1 < x:
      next_a_list[i] = True
    else:
      next_a_list[i] = False
  if n == 1:
    return next_a_list[0]
  else:
    return serch_dst(n-1, next_a_list)

def serch(not_dst, cost_list, n):
  next_cost_list = [False]*(3**(n-1))
  for i in range(3**(n-1)):
    tmp_cost_list = cost_list[i*3:i*3+3]
    tmp_cost_list.sort()
    next_cost_list[i] = tmp_cost_list[0] + tmp_cost_list[1]
  if n == 1:
    return next_cost_list[0]
  else:
    return serch(not_dst, next_cost_list, n-1)

def main():
  n = int(input())
  s = input()
  a_list = [False]*(3**n)
  for i in range(3**n):
    a_list[i] = int(s[i])
  ic(a_list)
  a_dst = serch_dst(n, a_list)
  ic(a_dst)
  not_dst = not(a_dst)
  if not_dst:
    for i in range(3**n):
      a_list[i] = 1 - a_list[i]
  # a_dstをnot_dstにするためのコストを伝播
  ans = serch(not_dst, a_list, n)
  print(ans)

if __name__ == "__main__":
  main()