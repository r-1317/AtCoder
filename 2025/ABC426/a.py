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
  d = {"Ocelot": 1, "Serval": 2, "Lynx": 3}

  ic(d["Lynx"])

  X, Y = input().split()

  print("Yes" if d[X] >= d[Y] else "No")

if __name__ == "__main__":
  main()