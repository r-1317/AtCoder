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
  a_list = list(map(int, input().split()))
  a_list.sort()
  sum_a = sum(a_list)

  ans_list = []

  # すべて分裂したと仮定
  flag = True
  if N%2 == 1:  # 奇数なら確実に違う
    flag = False
  else:
    l_kamo = a_list[0] + a_list[-1]
    for i in range(N//2):
      if a_list[i] + a_list[-1 -i] != l_kamo:
        flag = False
        break

  if flag:
    ans_list.append(l_kamo)

  # 分裂していないものがあると過程
  l_max = a_list[-1]
  while a_list and a_list[-1] == l_max:
    a_list.pop()

  flag = True
  if len(a_list)%2 == 1:  # 奇数なら確実に違う
    flag = False
  else:
    if len(ans_list) >= 2:
      l_max = a_list[0] + a_list[-1]
      for i in range(len(a_list)//2):
        if a_list[i] + a_list[-1 -i] != l_max:
          flag = False
          break
  
  if flag:
    ans_list.append(l_max)

  ans_list.sort()

  print(*ans_list)

if __name__ == "__main__":
  main()