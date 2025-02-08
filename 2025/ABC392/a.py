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
  a_list.sort()
  if a_list[0] * a_list[1] == a_list[2]:
    print("Yes")
  else:
    print("No")

if __name__ == "__main__":
  main()