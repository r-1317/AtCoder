import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  N, M = map(int, input().split())
  s_list = [(input()) for _ in range(N)]
  t_list = [(input()) for _ in range(M)]

  ic(s_list)
  ic(t_list)

  vote_list = [0]*N
  for t in t_list:
    near_list = []
    candidate = -1
    for i, s in enumerate(s_list):
      if len(s) == len(t):
        diff = 0
        for j in range(len(s)):
          if s[j] != t[j]:
            diff += 1
        if diff == 0:
          candidate = i
          break
        elif diff == 1:
          near_list.append(i)

    if candidate > -1:
      vote_list[candidate] += 1
    elif len(near_list) == 1:
      vote_list[near_list[0]] += 1

  for v in vote_list:
    print(v)


if __name__ == "__main__":
  main()