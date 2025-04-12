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

  s_list = [input() for _ in range(n)]

  status = False

  ans = 0

  for s in s_list:
    if s == "login":
      status = True
    elif s == "logout":
      status = False
    elif s == "private" and (not status):
      ans += 1

  print(ans)

if __name__ == "__main__":
  main()