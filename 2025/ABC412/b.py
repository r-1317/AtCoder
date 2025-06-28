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
  s = input().strip()
  t = input().strip()

  flag = True

  for i in range(1, len(s)):
    if s[i].isupper():
      u = s[i-1]
      if not u in t:
        flag = False
        break

  print("Yes" if flag else "No")


if __name__ == "__main__":
  main()