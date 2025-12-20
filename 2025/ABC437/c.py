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
    deer_list = [list(map(int, input().split())) for _ in range(N)]  # [[重さ, パワー], ...]

    deer_queue = list(range(N))  # queueといいながら普通のリスト

    deer_queue.sort(key=lambda x: deer_list[x][0] + deer_list[x][1])

    zanyo = sum([deer_list[i][0] for i in range(N)])
    ic(zanyo)
    for i in range(N, -1, -1):
      if zanyo <= 0:
        break
      zanyo -= sum(deer_list[deer_queue[i-1]])
    print(i)
    ic(i)


if __name__ == "__main__":
  main()