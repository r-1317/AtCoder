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
  n, k = map(int, input().split())
  a_list = list(map(int, input().split()))

  tmp = 1

  for a in a_list:
    tmp *= a
    if 10**k <= tmp:
      tmp = 1

  print(tmp)

if __name__ == "__main__":
  main()