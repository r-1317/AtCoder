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
  T = input()

  s_list = list(S)
  t_list = list(T)

  s_list_without_a = []
  for s in s_list:
    if s != "A":
      s_list_without_a.append(s)
  t_list_without_a = []
  for t in t_list:
    if t != "A":
      t_list_without_a.append(t)

  if s_list_without_a != t_list_without_a:
    print(-1)
    sys.exit()

  s_aidano_count = [0]*(len(s_list_without_a) + 1)
  t_aidano_count = [0]*(len(t_list_without_a) + 1)

  idx = 0
  for s in s_list:
    if s == "A":
      s_aidano_count[idx] += 1
    else:
      idx += 1
  
  idx = 0
  for t in t_list:
    if t == "A":
      t_aidano_count[idx] += 1
    else:
      idx += 1

  ic(s_aidano_count)
  ic(t_aidano_count)

  ans = 0

  for i in range(len(s_aidano_count)):
    sc = s_aidano_count[i]
    tc = t_aidano_count[i]

    ans += abs(sc-tc)

  print(ans)

if __name__ == "__main__":
  main()