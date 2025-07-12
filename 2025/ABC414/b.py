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

  ans_str = ""

  for _ in range(n):
    c, l = input().split()
    l = int(l)
    if len(ans_str) + l > 100:
      ans_str = "Too Long"
      break
    ans_str += c * l

  print(ans_str)

if __name__ == "__main__":
  main()