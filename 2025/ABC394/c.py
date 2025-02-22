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
  s = input()
  n = len(s)
  s_list = list(s)

  flag = False

  for i in range(n-1, -1, -1):
    if s_list[i] == "A":
      flag = True
    elif s_list[i] == "W" and flag:
      s_list[i] = "A"
      s_list[i+1] = "C"
      flag = True
    else:
      flag = False

  print(*s_list, sep="")

if __name__ == "__main__":
  main()