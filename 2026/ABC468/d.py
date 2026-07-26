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
  S = input()
  N = len(S)

  ans = 0


  for k in range(2):
    for i in range(N):
      l, r = i - k, i
      count = 0
      for j in range(N):
        if not(0 <= (l-j) and (r+j) < N):
          break
        if S[l-j] != S[r+j]:
          count += 1
          if count == 2:
            break
        ans += 1

  print(ans)

if __name__ == "__main__":
  main()