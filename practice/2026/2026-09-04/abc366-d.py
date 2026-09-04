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
  N = int(input())
  a_list = [[list(map(int, input().split())) for _ in range(N)] for _ in range(N)]

  cum_sum_1D = [[[0]*(N+1) for _ in range(N+1)] for _ in range(N+1)]
  cum_sum_2D = [[[0]*(N+1) for _ in range(N+1)] for _ in range(N+1)]
  cum_sum_3D = [[[0]*(N+1) for _ in range(N+1)] for _ in range(N+1)]

  # 1次元のを埋める
  for i in range(1, N+1):
    for j in range(1, N+1):
      for k in range(1, N+1):
        cum_sum_1D[i][j][k] = cum_sum_1D[i][j][k-1] + a_list[i-1][j-1][k-1]

  # 2次元のを埋める
  for i in range(1, N+1):
      for j in range(1, N+1):
        for k in range(1, N+1):
          cum_sum_2D[i][j][k] = cum_sum_2D[i][j-1][k] + cum_sum_1D[i][j][k]

  # 3次元のを埋める
  for i in range(1, N+1):
    for j in range(1, N+1):
      for k in range(1, N+1):
        cum_sum_3D[i][j][k] = cum_sum_3D[i-1][j][k] + cum_sum_2D[i][j][k]

  Q = int(input())
  for _ in range(Q):
    lx, rx, ly, ry, lz, rz = list(map(int, input().split()))  # Codonで実行できるようにlist形式

    # 大きいのを足す
    ans = cum_sum_3D[rx][ry][rz]

    # 各軸に垂直な面を引く
    ans -= cum_sum_3D[lx-1][ry][rz]  # x軸
    ans -= cum_sum_3D[rx][ly-1][rz]  # y軸
    ans -= cum_sum_3D[rx][ry][lz-1]  # z軸

    # 重複した部分を足す
    ans += cum_sum_3D[rx][ly-1][lz-1]  # x軸
    ans += cum_sum_3D[lx-1][ry][lz-1]  # y軸
    ans += cum_sum_3D[lx-1][ly-1][rz]  # z軸

    # 足しすぎた部分を再び引く
    ans -= cum_sum_3D[lx-1][ly-1][lz-1]

    # ic(ans)
    print(ans)

if __name__ == "__main__":
  main()