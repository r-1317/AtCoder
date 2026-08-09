import os
import sys

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
  s_t_list = [list(map(int, input().split())) for _ in range(N)]
  # s_t_list.sort()  # とりあえずソート(いらなかった)

  start_list = [[] for _ in range(2*N + 1)]
  end_list = [[] for _ in range(2*N + 1)]

  for i in range(N):
    s, t = s_t_list[i]
    start_list[s].append(i)
    end_list[t].append(i)

  current_meetings = []  # 現在やっている会議の数。2を超えたら即打ち切りなので要素数は少ない
  chunk_count = 0  # 途切れない会議の塊の数。2^chunk_countが答えになるはず

  for i in range(2*N+1):
    for c in end_list[i]:
      current_meetings.remove(c)
      if len(current_meetings) == 0:
        chunk_count += 1

    for c in start_list[i]:
      current_meetings.append(c)
      if len(current_meetings) > 2:
        print(0)
        sys.exit()

  print(2**chunk_count % 998244353)


if __name__ == "__main__":
  main()