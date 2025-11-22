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
  X = int(input())

  num_count = [0]*10

  for i in range(10):  # 過剰
    a = X%10
    num_count[a] += 1
    X //= 10
    if X == 0:
      break

  ans = ""

  for i in range(1, 10):
    if num_count[i] > 0:
      ans += str(i)
      num_count[i] -= 1
      break

  flag = True
  while flag:
    flag = False

    for i in range(10):
      if num_count[i] > 0:
        ans += str(i)
        num_count[i] -= 1
        flag = True
        break
    ic(num_count)

  print(ans)

if __name__ == "__main__":
  main()