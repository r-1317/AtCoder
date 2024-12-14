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
  n, c, d = input().split()
  n = int(n)
  s_list = list(input())
  for i in range(n):
    if s_list[i] != c:
      s_list[i] = d

  print(*s_list, sep="")

if __name__ == "__main__":
  main()