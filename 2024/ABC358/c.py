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

# 全ての味を手に入れる再帰関数
def search(n, m, get_list, s_list, store, first):
  
  ic(first, store)
  
  # この店で手に入る味をリストに追加
  for j in range(m):
    if s_list[store][j]:
      get_list[j] = True

  ic(get_list)

  # 全ての味を手に入れたら終了
  if all(get_list):
    return 1

  # その店で手に入る味の数をカウント
  count_list = [0]*n

  for i in range(n):
    for j in range(m):
      if s_list[i][j] and not get_list[j]:
        count_list[i] += 1

  ic(count_list)

  tmp = 10**9

  for i in range(n):
    if count_list[i] != 0:
      get_list_tmp = get_list[:]
      tmp = min(tmp, search(n, m, get_list_tmp, s_list, i, first) + 1)

  ic(store, tmp)

  return tmp

def main():
  n, m = map(int, input().split())  # n: 店の数  m: 味の数
  s_str_list = [(input()) for _ in range(n)]  # 店ごとの味の有無

  ic(s_str_list)

  s_list = [[False] * m for _ in range(n)]

  for i in range(n):
    for j in range(m):
      if s_str_list[i][j] == "o":
        s_list[i][j] = True

  ic(s_list)

  flag = True

  for i in range(n):
    if s_list[i].count(True) != 1:
      flag = False

  if flag and n == m:
    print(n)
    sys.exit()

  count_list = [0]*n  # その店で手に入る味の数

  ans = 10**9  # 行った店の数
  get_list = [False] * m  # 手に入れた味のリスト

  for i in range(n):
    get_list = [False] * m
    ans = min(ans, search(n, m, get_list, s_list, i, i))
    ic(i, ans)

  print(ans)

if __name__ == "__main__":
  main()