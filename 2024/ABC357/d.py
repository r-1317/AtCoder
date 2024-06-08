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
  n = int(input())
  num_digits = len(str(n))

  tmp = 0

  for i in range(n):
    tmp += n * 10**(num_digits*i)

  ic(tmp)

  ans = tmp % 998244353

  print(ans)

if __name__ == "__main__":
  main()