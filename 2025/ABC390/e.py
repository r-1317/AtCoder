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
  n, x = map(int, input().split())
  v_a_c_list = [list(map(int, input().split())) for _ in range(n)]

  dp_list = [[[-1, -1, -1] for _ in range(x+1)] for _ in range(3)]  # [最小値のindex][カロリー][ビタミンの種類]

  for v, a, c in v_a_c_list:
    v -= 1
    for j in range(3):
      for i in range(x-c):
        tmp_vitamin_list = dp_list[j][i][:]
        tmp_vitamin_list[v] += a
        min_amount = min(tmp_vitamin_list)
        for k in range(3):
          if tmp_vitamin_list != min_amount:
            continue
          if dp_list[k][i+c][k] < tmp_vitamin_list[v]:
            dp_list[k][i+c] = tmp_vitamin_list

    ic(dp_list)

  v1_max = dp_list[0][x][0]
  v2_max = dp_list[1][x][1]
  v3_max = dp_list[2][x][2]

  print(max(v1_max, v2_max, v3_max))

if __name__ == "__main__":
  main()