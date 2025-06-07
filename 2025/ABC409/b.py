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
  n = int(input())
  a_list = list(map(int, input().split()))
  count_list = [0]*102

  for a in a_list:
    if a < 101:
      count_list[int(a)] += 1
    else:
      count_list[101] += 1

  tmp_sum = 0
  ans = 0

  for i in range(101, -1, -1):
    tmp_sum += count_list[i]
    if i <= tmp_sum:
      ans = max(ans, i)

  print(ans)


if __name__ == "__main__":
  main()