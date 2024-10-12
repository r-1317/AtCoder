import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# xがs_listの中で最後に出現するインデックスを返す
def find_last_x(s_list, x):
  n = len(s_list)
  for i in range(n-1, -1, -1):
    if s_list[i] == x:
      return i
  return None

def main():
  s_list = list(input())
  n = len(s_list)
  ic(s_list)

  ans = 0

  # すべての大文字アルファベットについて
  for i in range(60,91):
    x = chr(i)
    last_x = find_last_x(s_list, x)
    ic(x, last_x)
    if last_x is None:
      continue
    x_count = 0  # xの出現回数
    tmp_count = 0  # 一時的なカウント
    new = False  # 直前でxが出現したか
    # すべての文字について
    for j in range(n):
      if s_list[j] == x:
        ans += tmp_count
      tmp_count += x_count
      if s_list[j] == x:
        x_count += 1

  print(ans)


if __name__ == "__main__":
  main()