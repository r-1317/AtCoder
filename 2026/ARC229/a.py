import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def count(s):
  for i in range(1, 10**9):
    flag = False
    for j in range(len(s) - 2):
      if s[j:j+3] == "ARC":
        flag = True
        s = s[:j] + "CRA" + s[j+3:]
        break
    if not flag:
      break
    # ic(s)

  return i - 1

def main():
  X = int(input())

  a_list = [1]*25 + [0]*25
  # ic(a_list)
  for i in range(625 - X):
    for j in range(len(a_list) - 1):
      if a_list[j] == 1 and a_list[j+1] == 0:
        a_list[j] = 0
        a_list[j+1] = 1
        break

  ans = ""
  for a in a_list:
    ans += "CA"[a]
    ans += "R"

  ic(count(ans))
  print(ans)

if __name__ == "__main__":  
  main()