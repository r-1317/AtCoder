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
  a_list = list(map(int, input().split()))
  ans = 0
  for i in range(1,5):
    if a_list.count(i) == 4:
      ans += 2
    elif a_list.count(i) >= 2:
      ans += 1

  print(ans)

if __name__ == "__main__":
  main()