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
  s_list = list(input())
  alphabet_list = [False] * 26
  for s in s_list:
    alphabet_list[ord(s) - ord("a")] = True

  for i in range(26):
    if not alphabet_list[i]:
      print(chr(i + ord("a")))
      exit()


if __name__ == "__main__":
  main()