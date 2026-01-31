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
  T = int(input())

  for _ in range(T):
    N = int(input())
    r_list = list(map(int, input().split()))
    is_visited = [False]*N
    kaisou_list = [[] for _ in range(N+1)]  # 自分の最低高さ
    for i in range(N):
      r = r_list[i]
      kaisou_list[r].append(i)

    min_height_list = [10**9]*N

    ic(kaisou_list)

    for i in range(N+1):
      for k in kaisou_list[i]:
        if is_visited[k]:
          continue
        min_height_list[k] = i

        if i < N:
          if k > 0 and  not is_visited[k-1]:
            kaisou_list[i+1].append(k-1)
          if k < N-1 and not is_visited[k+1]:
            kaisou_list[i+1].append(k+1)
        
        is_visited[k] = True

    ic(min_height_list)
    ic(r_list)

    ans = 0
    for i in range(N):
      ans += r_list[i] - min_height_list[i]

    ic(ans)
    print(ans)


if __name__ == "__main__":
  main()