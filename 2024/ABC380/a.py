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

  list_n = list(str(n))

  if list_n.count("1") == 1 and list_n.count("2") == 2 and list_n.count("3") == 3:
    print("Yes")
  else:
    print("No")

if __name__ == "__main__":
  main()