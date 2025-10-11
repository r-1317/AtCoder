import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

count = 0

def r(N, M, a_list, tmp_mod, last, current_idx, state):
  global count
  if current_idx == N:
    if tmp_mod == 0:
      count += 1
    return True

  # そうでない場合
  if state:
    if last == current_idx - 1:
      return False
    else:
      tmp_mod += a_list[current_idx]
      tmp_mod %= M
      last = current_idx

  r(N, M, a_list, tmp_mod, last, current_idx+1, 0)
  r(N, M, a_list, tmp_mod, last, current_idx+1, 1)

def main():
  N, M = map(int, input().split())
  a_list = list(map(int, input().split()))

  r(N, M, a_list, 0, -100, 0, 0)
  r(N, M, a_list, 0, -100, 0, 1)

  print(count//2)

if __name__ == "__main__":
  main()