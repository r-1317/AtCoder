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
  S, A, B, X = map(int, input().split())

  ans = 0

  arr = [B, A]

  state = 1
  step = 0

  for i in range(X):
    if state:
      ans += S

    step += 1

    if step == arr[state]:
      state = not state
      step = 0

  print(ans)


if __name__ == "__main__":
  main()