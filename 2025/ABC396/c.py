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
  n, m = map(int, input().split())
  b_list = list(map(int, input().split()))
  w_list = list(map(int, input().split()))

  b_list.sort(reverse=True)
  w_list.sort(reverse=True)

  max_num = 0
  tmp_num = 0
  w_flag = True

  for i in range(n):
    if w_flag:
      if i == m:
        w_flag = False
      elif w_list[i] < 0:
        w_flag = False
    tmp_num += b_list[i]
    if w_flag:
      tmp_num += w_list[i]
    if max_num < tmp_num:
      max_num = tmp_num

  print(max_num)


if __name__ == "__main__":
  main()