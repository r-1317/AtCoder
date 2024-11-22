import os
import sys

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

  if n % 2 == 1:
    print("No")
    sys.exit()

  char_count_list = [0] * 26
  flag = True

  for i in range(n//2):
    if s[2*i] != s[2*i+1]:
      flag = False
      break
    char_count_list[ord(s[2*i]) - ord("a")] += 2

  ic(flag)

  for char_count in char_count_list:
    if char_count != 0 and char_count != 2:
      flag = False
      break

  ic(flag)

  print("Yes" if flag else "No")



if __name__ == "__main__":
  main()