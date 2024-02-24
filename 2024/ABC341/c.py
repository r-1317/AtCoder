import copy

def calc_dist(t, n):
  t_list = [[0,0] for _ in range(n)]
  tmp = [0,0]

  # 移動した距離を求める
  for i in range(n):

    # 左に移動
    if t[i] == "L":
      tmp[1] -= 1

    # 右に移動
    elif t[i] == "R":
      tmp[1] += 1

    # 上に移動
    elif t[i] == "U":
      tmp[0] -= 1

    # 下に移動
    elif t[i] == "D":
      tmp[0] += 1

    t_list[i] = copy.deepcopy(tmp)  # 移動iをした時点での総移動距離
    # print(f"tmp({i}): {tmp}")  # デバッグ
    # print(f"t_list({i}): {t_list}")  # デバッグ
    

  # print(t_list)  # デバッグ

  return t_list

# 高橋君が現在いるマスとしてあり得るか否か
def is_possible(i, j, t_list, s_list, n):

  # 最初から海ならFalse
  if s_list[i][j] == "#":
    return False

  # 1つでも海ならFalse
  for k in range(n):

    if s_list[i+t_list[k][0]][j+t_list[k][1]] == "#":
      return False

  # 1つも海がなければTrue
  return True


def main():
  h, w, n = map(int, input().split())
  t = input()  # 移動の内容
  s_list = [(input()) for _ in range(h)]  # 長さwの文字列h個からなるリスト
  ans = 0  # あり得るマスの数

  t_list = calc_dist(t, n)  # それぞれの移動をした時点での総移動距離

  for i in range(1, h-1):  # 縦のループ
    for j in range(1, w-1):  # 横のループ

      # マス(i,j)が現在いるマスとしてあり得るなら解答に1を追加
      if is_possible(i, j, t_list, s_list, n):
        ans += 1

  print(ans)


if __name__ == "__main__":
  main()