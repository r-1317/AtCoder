import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

henkan = [2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9]

def main():
  N = int(input())
  s_list = list(input().split())

  ans = ""

  for s in s_list:
    c = henkan[ord(s[0]) - 97]
    ans += str(c)

  print(ans)

if __name__ == "__main__":
  main()