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
  a, b, c = map(int, input().split())
  s_set = {a, b, c}
  if len(s_set) < 3:
    print("Yes")
  else:
    print("No")

if __name__ == "__main__":
  main()