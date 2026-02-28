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
  S = input()
  s_list = list(S)

  freq_list = [0]*200

  for s in s_list:
    freq_list[ord(s)] += 1

  max_count = max(freq_list)

  ans = ""

  for s in s_list:
    if freq_list[ord(s)] != max_count:
      ans += s

  print(ans)

if __name__ == "__main__":
  main()