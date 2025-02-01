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
  d = input()
  list_1 = ["N", "E", "S", "W"]
  list_2 = ["NE", "NW", "SW", "SE"]
  if d in list_1:
    print(list_1[(list_1.index(d) + 2) % 4])
  else:
    print(list_2[(list_2.index(d) + 2) % 4])

if __name__ == "__main__":
  main()