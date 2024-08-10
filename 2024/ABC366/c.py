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
  q_list = [list(map(int, input().split())) for _ in range(n)]

  count_list = [0]*(10**6+1)

  ans = 0

  for i in range(n):
    q = q_list[i][0]
    if q != 3:
      x = q_list[i][1]

    if q == 1:
      count_list[x] += 1
      if count_list[x] == 1:
        ans += 1

    elif q == 2:
      count_list[x] -= 1
      if count_list[x] == 0:
        ans -= 1

    if q == 3:
      print(ans)
      ic(ans)

if __name__ == "__main__":
  main()