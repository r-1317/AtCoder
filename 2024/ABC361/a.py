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
  n, k, x = map(int, input().split())
  a_list = list(map(int, input().split()))

  a_list.insert(k, x)

  print(*a_list)

if __name__ == "__main__":
  main()