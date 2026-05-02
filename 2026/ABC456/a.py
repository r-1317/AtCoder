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
  X = int(input())

  flag = False

  for i in range(1, 7):
    for j in range(1, 7):
      for k in range(1, 7):
        if i + j + k == X:
          flag = True
  
  print("Yes" if flag else "No")

if __name__ == "__main__":
  main()