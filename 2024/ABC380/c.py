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
  n, k = map(int, input().split())
  s_list = list(input())

  current = "0"
  count = 0

  j_tail = 0
  k_head = 0
  k_tail = n  # 最後まで更新されない場合はnとなる

  for i in range(n):
    if s_list[i] == "1" and current == "0":
      count += 1
      if count == k:
        k_head = i
    elif s_list[i] == "0" and current == "1":
      if count == k:
        k_tail = i
      elif count == k-1:
        j_tail = i
    current = s_list[i]

  ic(k_head, j_tail, k_tail)

  ans_list = s_list[:j_tail] + s_list[k_head:k_tail] + s_list[j_tail:k_head] + s_list[k_tail:]

  print(*ans_list, sep="")


if __name__ == "__main__":
  main()