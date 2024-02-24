import copy

# topより小さい最大値を返す
def find_max_less_than(d_list, top):

  # d_listを複製
  tmp_list = copy.deepcopy(d_list)

  # top以上の要素を0に
  for i in range(len(tmp_list)):

    # top以上は除外
    if top <= tmp_list[i]:
      tmp_list[i] = 0  # 実質除外
  
  return max(tmp_list)  # top未満の中で最大値

# メイン処理
def main():

  n = int(input())  # 餅の数
  d_list = [int(input()) for _ in range(n)]  # 餅の直径のリスト
  top = 101  # 最上位の餅の直径。初期値は餅の直径の最大値より大きい
  ans = 0  # 餅の段数

  # print(f"d_list: {d_list}")  # デバッグ

  # 餅を重ねる
  while min(d_list) < top:  # 最上位より小さい餅が存在する

    top = find_max_less_than(d_list, top)  # 最上位を更新
    d_list[d_list.index(top)] = 102  # 取った餅を使えなくする
    ans += 1  # 段数を追加

  #解答の出力
  # print(f"最終: {d_list}")  # デバッグ
  print(ans)

if __name__ == "__main__":
  main()