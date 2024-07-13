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
  rgb_list = list(map(int, input().split()))
  c = input()

  if c == "Red":
    rgb_list[0] = 10**9
  elif c == "Green":
    rgb_list[1] = 10**9
  else:
    rgb_list[2] = 10**9

  print(min(rgb_list))

if __name__ == "__main__":
  main()