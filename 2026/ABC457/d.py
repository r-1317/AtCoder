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

  min_a = 2**60  # 多分これで行けるはず
  stride = 2**59

  valid_max = -1

  while True:
    ic(min_a, stride)
    count = 0
    for i, a in enumerate(a_list):
      if a > min_a:  # ここ不安
        continue
      count += (min_a - a) // (i+1)
      if (min_a - a) % (i+1) > 0:  # あまりの処理
        count += 1
    if count <= K:
      valid_max = max(valid_max, min_a)
      min_a += stride
    else:
      min_a -= stride
    if stride == 0:  # 二分探索終了
      break
    stride //= 2

  print(valid_max)

if __name__ == "__main__":
  main()