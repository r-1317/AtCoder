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

  # nest_set_list = [set() for _ in range(n)]  # 巣を集合で管理。これの順番は変えない
  index_nest_list = [i for i in range(n+1)]  # 巣のインデックスを管理。巣iの中身がnest_set_list[i]になる
  nest_index_list = [i for i in range(n+1)]  # index_nest_listの逆引き。
  pigeon_list = [i for i in range(n+1)]  # 鳩のリスト。鳩iの巣はnest_set_list[pigeon_list[i]]になる

  for i in range(1, q+1):
    query = list(map(int, input().split()))
    # 種類1のクエリの場合、鳩aを巣bに移す
    if query[0] == 1:
      a, b = query[1], query[2]
      next_nest = index_nest_list[b]
      pigeon_list[a] = next_nest
    # 種類2のクエリの場合、巣aと巣bを入れ替える
    elif query[0] == 2:
      a, b = query[1], query[2]
      index_nest_list[a], index_nest_list[b] = index_nest_list[b], index_nest_list[a]
      nest_index_list[index_nest_list[a]], nest_index_list[index_nest_list[b]] = nest_index_list[index_nest_list[b]], nest_index_list[index_nest_list[a]]
    # 種類3のクエリの場合、鳩aの巣を出力
    else:
      a = query[1]
      # ic(i, a, pigeon_list[index_nest_list[a]])
      # print(pigeon_list[nest_index_list[a]])  # 間違い
      print(nest_index_list[pigeon_list[a]])
      ic(nest_index_list[pigeon_list[a]])
    # if MyPC and i == 4:
    #   debug_list = [pigeon_list[nest_index_list[i]] for i in range(1, n+1)]
    #   ic(i)
    #   ic(pigeon_list[1:])
    #   ic(nest_index_list[1:])
    #   ic(debug_list)
    #   ic(pigeon_list[nest_index_list[2]], pigeon_list[nest_index_list[4]])

if __name__ == "__main__":
  main()