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
  N, M = map(int, input().split())
  x_list = list(map(int, input().split()))

  imos_list = [0]*N  # 島iと島(i+1)modNを結ぶ橋の封鎖コスト

  prev_cost = 0

  for i in range(M-1):
    cur_pos = x_list[i] - 1
    new_pos = x_list[i+1] - 1

    p1 = min(cur_pos, new_pos)
    p2 = max(cur_pos, new_pos)

    cost = None
    if p2 - p1 < p1 + N - p2:
      cost = p2 - p1
      prev_cost += cost
      imos_list[p1] += N - cost*2
      imos_list[p2] -= N - cost*2
    else:
      cost = p1 + N - p2
      prev_cost += cost
      imos_list[p2] += N - cost*2
      imos_list[0] += N - cost*2
      imos_list[p1] -= N - cost*2

  cost_list = []

  current_cost = 0

  for i in range(N):
    current_cost += imos_list[i]
    cost_list.append(current_cost)

  print(prev_cost + min(cost_list))


if __name__ == "__main__":
  main()