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
  N = int(input())
  S = input()

  one_idx_list = []
  for i in range(N):
    if S[i]== "1":
      one_idx_list.append(i)

  mid_idx = len(one_idx_list) // 2
  l_list = one_idx_list[:mid_idx]
  l_list = l_list[::-1]
  r_list = one_idx_list[mid_idx + 1:]
  mid = one_idx_list[mid_idx]

  ic(mid)
  ic(l_list)
  ic(r_list)

  ans = 0

  for i, l in enumerate(l_list):
    ans += mid - l - i - 1

  for i, r in enumerate(r_list):
    ans += r - mid - i - 1

  print(ans)

if __name__ == "__main__":
  main()