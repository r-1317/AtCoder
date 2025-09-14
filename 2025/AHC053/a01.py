import os
from typing import Tuple

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

N = 500
M = 50
L = 10**15 - 2*10**12
U = 10**15 + 2*10**12

def main():
  _, _, _, _ = map(int, input().split())

  a_list = []  # i番目のカードの値
  x_list = [0] * N  # i番目のカードが属する山
  stride = (U - L) // 2

  for i in range(M):
    a_list.append(L)
  
  for i in range(N//M - 1):
    for j in range(M):
      a_list.append(stride)
    stride //= 2
    

  ic(len(a_list))
  print(*a_list)

  b_list = list(map(int, input().split()))  # i番目の山の合計値の目標

  # x_listを一部埋める
  for i in range(M):
    x_list[i] = i+1

  # 出力
  print(*x_list)

if __name__ == "__main__":
  main()