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

  ans = 0

  count = 0
  prev_char = ""

  for c in list(S):
    if c != prev_char:
      count += 1
    else:
      count = 1
    ans += count
    prev_char = c

  print(ans % 998244353)

if __name__ == "__main__":
  main()