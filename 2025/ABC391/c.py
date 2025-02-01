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
  pigeon_list = [i for i in range(n + 1)]  # 鳩iがいる巣の番号
  nest_list = [1] * (n+1)  # 巣iにいる鳩の数
  ans = 0

  for _ in range(q):
    query = list(map(int, input().split()))
    # 楽なので、クエリ2の処理を先に書く
    if query[0] == 2:
      print(ans)
    # クエリ1の処理
    else:
      _, p, h = query
      # 鳩pを巣hに移動
      nest_list[pigeon_list[p]] -= 1
      if nest_list[pigeon_list[p]] == 1:
        ans -= 1
      pigeon_list[p] = h
      nest_list[h] += 1
      if nest_list[h] == 2:
        ans += 1
    # ic(query, pigeon_list, nest_list, ans)


if __name__ == "__main__":
  main()