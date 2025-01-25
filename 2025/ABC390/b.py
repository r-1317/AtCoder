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

  for i in range(n):
    a_list[i] *= 10**9

  r = a_list[1] / a_list[0]
  b_list = [0]*n
  b_list[0] = a_list[0]

  for i in range(1, n):
    b_list[i] = b_list[i-1] * r

  flag = True

  for i in range(n):
    if abs(a_list[i] - b_list[i]) > 10**(-6):
      flag = False
      break

  print("Yes" if flag else "No")

if __name__ == "__main__":
  main()