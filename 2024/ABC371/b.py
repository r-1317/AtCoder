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
  n, m = map(int, input().split())
  flag_list = [False] * n

  for m in range(m):
    a, b = input().split()
    a = int(a)

    if (not flag_list[a - 1]) and b == "M":
      flag_list[a - 1] = True
      print("Yes")
    else:
      print("No")



if __name__ == "__main__":
  main()