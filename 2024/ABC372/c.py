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
  n, q = map(int, input().split())
  s = input()
  s_list = list(s)
  ic(s_list)

  ABC_list = [False]*(n-2)  # index番目から始まる3文字がABCかどうか

  for i in range(n-2):
    if s_list[i] == "A" and s_list[i+1] == "B" and s_list[i+2] == "C":
      ABC_list[i] = True

  ans = sum(ABC_list)
  ic(ABC_list)
  ic(ans)

  for _ in range(q):
    x, c = input().split()
    x = int(x) - 1  # indexを0始まりにする

    s_list[x] = c

    for i in range(x-2, x+3):
      if 0 <= i < n-2:
        if s_list[i] == "A" and s_list[i+1] == "B" and s_list[i+2] == "C":
          ans += not(ABC_list[i])  # 今までABCではなかったら+1
          ABC_list[i] = True
        else:
          ans -= ABC_list[i]  # 今までABCだったら-1
          ABC_list[i] = False

    print(ans)


if __name__ == "__main__":
  main()