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
  s_list = [False]*len(s)

  for i, s in enumerate(s):
    if s == "i":
      s_list[i] = True
    else:
      s_list[i] = False

  tmp = False

  ans = 0

  for i , s in enumerate(s_list):
    if s:
      if tmp:
        ans += 1
      tmp = True
    else:
      if not tmp:
        ans += 1
      tmp = False

  if (len(s_list) + ans) % 2:
    ans += 1
  elif s_list[-1]:
    ans += 1

  print(ans)


if __name__ == "__main__":
  main()