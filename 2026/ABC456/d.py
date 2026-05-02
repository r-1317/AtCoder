import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def c_to_idx(c):
  return ord(c) - 97

def main():
  S = input()

  ans = 0

  prev_char = ""
  char_count = [0, 0, 0]

  for i, c in enumerate(list(S)):
    if c == prev_char:
      renzoku += 1
    else:
      renzoku = 0
    
    ans += 2**(i - renzoku)
    ans %= 998244353

  ans %= 998244353  # 念の為
  print(ans)

if __name__ == "__main__":
  main()