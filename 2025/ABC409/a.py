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
  takahashi_list = list(input())
  aoki_list = list(input())

  flag = False

  for i in range(n):
    if takahashi_list[i] == "o" and aoki_list[i] == "o":
      flag = True
      break

  print("Yes" if flag else "No")

if __name__ == "__main__":
  main()