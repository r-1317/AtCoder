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
  n, m = map(int, input().split())
  a_list = list(map(int, input().split()))

  ans = 0

  for i in range(n):
    flag = True
    for j in range(1, m+1):
      flag2 = False
      for k in range(len(a_list)):
        ic(k, j)
        if a_list[k] == j:
          flag2 = True
          break
      if not flag2:
        flag = False
        break
    if not flag:
      print(ans)
      exit()
    a_list = a_list[:-1]
    ans += 1
  
  print(ans)

if __name__ == "__main__":
  main()