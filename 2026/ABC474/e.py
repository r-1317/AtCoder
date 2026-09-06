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
    a_b_list = [list(map(int, input().split())) for _ in range(N)]
    a_list = [a_b[0] for a_b in a_b_list]
    b_list = [a_b[1] for a_b in a_b_list]

    min_a = min(a_list)

    d_list = [-1]*N
    for i in range(N):
      d_list[i] = a_list[i] - b_list[i]

    d_list.sort()  # 順番はここで崩してもいいかな。多分いいと思う
    half_N = N // 2  # 最小のクーポンの数
    for _ in range(half_N):
      d_list.pop()

    ic(d_list)
    rem = N - half_N * 2  # クーポンの余り
    ic(rem)

    count = 0
    while d_list[-1] > min_a*(2 - rem):
      d_list.pop()
      count += 2 - rem
      # if rem <= 0:
      #   count += 1
      #   rem += 1
      # else:
      #   rem -= 1
      if rem:
        rem = 0

    ans = sum(b_list) + sum(d_list) + min_a * count
    ic(ans)
    print(ans)

if __name__ == "__main__":
  main()