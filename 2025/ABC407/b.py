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
  x, y = map(int, input().split())

  x_count = 0
  y_count = 0
  xy_count = 0

  for i in range(1, 7):
    for j in range(1, 7):
      flag = False
      if x <= (i+j):
        x_count += 1
        flag = True
      if y <= abs(i-j):
        y_count += 1
        if flag:
          xy_count += 1

  prob = (x_count + y_count - xy_count) / 36

  print(prob)

if __name__ == "__main__":
  main()