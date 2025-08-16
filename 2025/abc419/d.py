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
  S = input()
  T = input()
  swap_list = [0] * (N + 1)

  for _ in range(M):
    l, r = map(int, input().split())
    l -= 1
    # rは+1しておきたいので、そのまま
    swap_list[l] += 1
    swap_list[r] -= 1

    ic(swap_list)

  ans = []

  state = 0

  for i in range(N):
    state += swap_list[i]
    if state % 2 == 1:
      ans.append(T[i])
    else:
      ans.append(S[i])

  print("".join(ans))

if __name__ == "__main__":
  main()