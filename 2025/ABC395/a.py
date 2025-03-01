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
  a_list = list(map(int, input().split()))

  flag = True

  for i in range(n-1):
    if not (a_list[i] < a_list[i+1]):
      flag = False
      break

  print("Yes" if flag else "No")

if __name__ == "__main__":
  main()