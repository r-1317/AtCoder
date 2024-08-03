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

  sorted_a_list = sorted(a_list)


  print(a_list.index(sorted_a_list[-2])+1)

if __name__ == "__main__":
  main()