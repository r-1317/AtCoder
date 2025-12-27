import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def get_cum_sum(arr):
  return_arr = [-1] * len(arr)
  return_arr[0] = arr[0]

  for i in range(1, len(arr)):
    return_arr[i] = return_arr[i-1] + arr[i]

  return return_arr

def main():
  N = int(input())
  a_list = list(map(int, input().split()))
  b_list = list(map(int, input().split()))
  c_list = list(map(int, input().split()))

  a_cum_sum = get_cum_sum(a_list)
  b_cum_sum = get_cum_sum(b_list)
  c_cum_sum = get_cum_sum(c_list)

  sa_list = [0]*N
  for i in range(N):
    sa_list[i] = a_list[i] - b_list[i]

  sa_cum_sum = get_cum_sum(sa_list)

  x_idx_list = [None]*N  # y = i のときの x

  x_idx_list[1] = 0
  max_sacum = sa_cum_sum[0]

  for i in range(1, N-1):
    sacum = sa_cum_sum[i]
    if max_sacum < sacum:
      max_sacum = sacum
      x_idx_list[i+1] = i
    else:
      x_idx_list[i+1] = x_idx_list[i]

  ic(x_idx_list)

  max_score = 0

  for y in range(1, N-1):
    score = 0
    x = x_idx_list[y]

    score += a_cum_sum[x]

    score += b_cum_sum[y]
    score -= b_cum_sum[x]

    score += c_cum_sum[-1]
    score -= c_cum_sum[y]

    max_score = max(max_score, score)

  print(max_score)

if __name__ == "__main__":
  main()