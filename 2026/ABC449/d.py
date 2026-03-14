import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def is_black(a):
  if abs(a) % 2 == 0:
    return 1
  else:
    return 0

def main():
  L, R, D, U = map(int, input().split())

  shape = [R - L + 1, U - D + 1]  # 長方形の大きさ(格子点の数で見た際の)

  x_bandwidth = [L, R]
  y_bandwidth = [D, U]

  ans = 0

  # while x_bandwidth[0] != x_bandwidth[1] or y_bandwidth[0] != y_bandwidth[1]:
  while shape[0] and shape[1]:
    max_abs = max(abs(x_bandwidth[0]), abs(x_bandwidth[1]), abs(y_bandwidth[0]), abs(y_bandwidth[1]))

    if abs(x_bandwidth[0]) == max_abs and shape[0]:
      ic(x_bandwidth[0], shape[1])
      ans += shape[1] * is_black(x_bandwidth[0])
      x_bandwidth[0] += 1
      shape[0] -= 1
    elif abs(x_bandwidth[1]) == max_abs and shape[0]:
      ic(x_bandwidth[1], shape[1])
      ans += shape[1] * is_black(x_bandwidth[1])
      x_bandwidth[1] -= 1
      shape[0] -= 1
    elif abs(y_bandwidth[0]) == max_abs  and shape[1]:
      ic(y_bandwidth[0], shape[0])
      ans += shape[0] * is_black(y_bandwidth[0])
      y_bandwidth[0] += 1
      shape[1] -= 1
    elif abs(y_bandwidth[1]) == max_abs  and shape[1]:
      ic(y_bandwidth[1], shape[0])
      ans += shape[0] * is_black(y_bandwidth[1])
      y_bandwidth[1] -= 1
      shape[1] -= 1

    if not(shape[0] or shape[1]):
      ans += is_black(max(abs(x_bandwidth[0]), y_bandwidth[0]))

  

  print(ans)



if __name__ == "__main__":
  main()