import os
import itertools

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

# ic.enable() if MyPC else None

CHEMICALS = list(range(18))

def main():
  T = int(input())
  for _ in range(T):
    N = int(input())
    S = input()
    S = "0" + S + "0"

    state_quered = [0]

    for i in range(N):
      next_quere = []
      for state in state_quered:
        for j in range(N):
          if (state >> j) & 1:
            continue
          next_state = state
          next_state += 1 << j
          ic(next_state, j)
          if S[next_state] == "0":
            next_quere.append(next_state)
            ic(next_state, S[next_state])
      state_quered = next_quere
      ic(state_quered)
    if len(state_quered) == 0:
      print("No")
    else:
      print("Yes")


if __name__ == "__main__":
  main()