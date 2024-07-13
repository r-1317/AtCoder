import os
import math
import numpy as np

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  # 点a, b, cのx,y座標
  a_coord = list(map(int, input().split()))
  b_coord = list(map(int, input().split()))
  c_coord = list(map(int, input().split()))

  # ベクトルab, acを求める
  ab = np.array(b_coord) - np.array(a_coord)
  ac = np.array(c_coord) - np.array(a_coord)
  # ベクトルab, acの内積を求める
  a_inner_product = np.inner(ab, ac)

  # ベクトルba, bcを求める
  ba = np.array(a_coord) - np.array(b_coord)
  bc = np.array(c_coord) - np.array(b_coord)
  # ベクトルba, bcの内積を求める
  b_inner_product = np.inner(ba, bc)

  # ベクトルca, cbを求める
  ca = np.array(a_coord) - np.array(c_coord)
  cb = np.array(b_coord) - np.array(c_coord)
  # ベクトルca, cbの内積を求める
  c_inner_product = np.inner(ca, cb)

  ic(type(a_inner_product))

  ic(a_inner_product, b_inner_product, c_inner_product )

  if not (a_inner_product and b_inner_product and c_inner_product):
    print("Yes")
  else:
    print("No")


if __name__ == "__main__":
  main()