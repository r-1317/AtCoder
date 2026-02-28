import os
import sys

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  S = input()
  s_list = list(S)

  # a_idx = -1
  # b_idx = -1
  # c_idx = -1

  a_idx_list = []
  b_idx_list = []
  c_idx_list = []

  for i in range(len(s_list)):
    s = s_list[i]
    if s == "A":
      a_idx_list.append(i)
    elif s == "B":
      b_idx_list.append(i)
    elif s == "C":
      c_idx_list.append(i)

  if not(a_idx_list and b_idx_list and c_idx_list):
    print(0)
    sys.exit()

  a_idx_list.reverse()
  b_idx_list.reverse()
  c_idx_list.reverse()

  a_idx = a_idx_list.pop()
  b_idx = b_idx_list.pop()
  c_idx = c_idx_list.pop()

  ans = 0

  while True:
    if a_idx < b_idx < c_idx:
      ans += 1
      if not(a_idx_list and b_idx_list and c_idx_list):
        break
      a_idx = a_idx_list.pop()
      b_idx = b_idx_list.pop()
      c_idx = c_idx_list.pop()
    if b_idx <= a_idx:
      if not b_idx_list:
        break
      b_idx = b_idx_list.pop()
    if c_idx <= b_idx:
      if not c_idx_list:
        break
      c_idx = c_idx_list.pop()
  
  print(ans)


if __name__ == "__main__":
  main()