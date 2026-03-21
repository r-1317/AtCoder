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
  N, K = map(int, input().split())
  a_list = list(map(int, input().split()))

  max_a = max(a_list)

  ic(max_a)

  count = 0  # 回数。答えだと勘違いしていたけれど違った

  for i in range(N):
    diff = max_a - a_list[i]
    kaisuu = diff // K
    a_list[i] += K * kaisuu
    count += kaisuu

  ans = max(a_list) - min(a_list)

  a_list.sort()

  ic(a_list)

  for i in range(N-1):
    ans = min(ans, a_list[i] + K - a_list[i+1])

  print(ans)


if __name__ == "__main__":
  main()