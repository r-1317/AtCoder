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
  S = input()

  cum_sum_list = [0]*N
  cum_sum_list[0] = 1 if S[0] == "o" else 0
  for i in range(1, N):
    cum_sum_list[i] = cum_sum_list[i-1] + (1 if S[i] == "o" else 0)

  ic(cum_sum_list)

  for i in range(N):
    prev_pos = 0
    pos = i
    hit_count = cum_sum_list[i]  # あたりの数
    while hit_count:
      new_pos = min(pos + hit_count, N-1)
      new_hit_count = cum_sum_list[new_pos] - cum_sum_list[pos]
      # 値の更新
      pos = new_pos
      hit_count = new_hit_count
      if pos == N-1:
        break
    print(pos+1)


if __name__ == "__main__":
  main()