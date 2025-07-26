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
    N, M = map(int, input().split())
    A_list = list(map(int, input().split()))
    B_list = list(map(int, input().split()))

    A_list.sort(reverse=True)
    B_list.sort()

    ic(A_list)
    ic(B_list)

    i = 0
    index = 0
    count = 0
    fill_count = 0

    for a in A_list:
      mod_min = M - a
      while i < N and B_list[i] < mod_min:  # ここ動くか怪しい
        i += 1
      # 丁度いいB_iが見つかった場合
      if i < N:
        count += 1
        index = i
        fill_count += 1
        i += 1
      else:  # ここでB_iが見つからなかった場合は、最後まで見つからないため、終了
        # i = max(index + 1, fill_count)
        # fill_count += 1
        break

    ic(count)
    ic(fill_count)

    ans = sum(A_list) + sum(B_list) - count * M
    ic(ans)
    print(ans)

if __name__ == "__main__":
  main()