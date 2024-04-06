from icecream import ic

def calc_dist(point, points_list, n):
  dist_list = [0]*n

  # 点jまでの距離を求める
  for j in range(n):
    dist = (point[0] - points_list[j][0])**2 + (point[1] - points_list[j][1])**2

    dist_list [j] = dist

  return dist_list.index(max(dist_list)) + 1


def main():
  n = int(input())
  points_list = [list(map(int, input().split())) for _ in range(n)]

  # 点iから最も遠い点を探す
  for i in range(n):
    farthest = calc_dist(points_list[i], points_list, n)
    print(farthest)



if __name__ == "__main__":
  main()