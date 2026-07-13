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
  T = int(input())

  for _ in range(T):
    k = int(input())
    ans = k

    while str(ans).count("00") == 0:
      ans += k

    ic(ans)
    print(ans)

if __name__ == "__main__":
  main()