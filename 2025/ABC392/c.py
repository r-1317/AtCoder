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
  p_list = list(map(int, input().split()))  # 人iが見ている人の番号
  q_list = list(map(int, input().split()))  # 人iが着ているゼッケンの番号
  for i in range(n):
    p_list[i] -= 1
    q_list[i] -= 1
  ic(p_list)
  ic(q_list)
  wearer_list = [0] * n
  for i, q in enumerate(q_list):
    wearer_list[q] = i
  ic(wearer_list)

  ans_list = [0]*n
  for i in range(n):
    x = wearer_list[i]
    y = p_list[x]
    z = q_list[y]
    ans_list[i] = z + 1
  print(*ans_list)


if __name__ == "__main__":
  main()