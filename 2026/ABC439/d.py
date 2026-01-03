import os
import bisect

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
  a_list = list(map(int, input().split()))

  three_dict = {}
  seven_dict = {}

  for i in range(N):
    a = a_list[i]

    a3 = a * 5 * 7
    if not a3 in three_dict:
      three_dict[a3] = []  # 空配列で初期化
    three_dict[a3].append(i)

    a7 = a * 3 * 5
    if not a7 in seven_dict:
      seven_dict[a7] = []  # 空配列で初期化
    seven_dict[a7].append(i)

  ic(three_dict)
  ic(seven_dict)

  # カウント
  ans = 0
  for i in range(N):
    a = a_list[i]
    a5 = a * 3 * 7
    if not ((a5 in three_dict) and (a5 in seven_dict)):
      continue
    # iが最大indexの場合
    max_3_count = bisect.bisect(three_dict[a5], i)
    max_7_count = bisect.bisect(seven_dict[a5], i)
    ans += max_3_count * max_7_count

    # iが最小indexの場合
    min_3_count = len(three_dict[a5]) - max_3_count
    min_7_count = len(seven_dict[a5]) - max_7_count
    ans += min_3_count * min_7_count
  
  print(ans)

if __name__ == "__main__":
  main()