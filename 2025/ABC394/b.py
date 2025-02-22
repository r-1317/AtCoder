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
  s_list = [input() for _ in range(n)]

  sorted_s_list = [""]*100

  for i, s in enumerate(s_list):
    sorted_s_list[len(s)] = s

  print(*sorted_s_list, sep="")

if __name__ == "__main__":
  main()