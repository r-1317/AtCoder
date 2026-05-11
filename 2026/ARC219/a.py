import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def rev(s):
  rev_s = ""
  for c in list(s):
    rev_c = "0" if c == "1" else "1"
    rev_s += rev_c
  return rev_s

def get_ans(ng_set, M, t):  # dfs
  if len(t) == M:
    # ic(t)
    if t in ng_set:
      return None
    else:
      return t
  
  next_t_0 = get_ans(ng_set, M, t+"0")
  if next_t_0 is not None:
    return next_t_0
  next_t_1 = get_ans(ng_set, M, t+"1")
  if next_t_1 is not None:
    return next_t_1
  else:
    return None

def main():
  N, M = map(int, input().split())
  s_list = [input() for _ in range(N)]

  ng_set = set()

  for s in s_list:
    rev_s = rev(s)
    ic(rev_s)
    ng_set.add(rev_s)

  ans = get_ans(ng_set, M, "")

  if ans is None:
    print("No")
  else:
    print("Yes")
    print(ans)

if __name__ == "__main__":
  main()