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
  h_list = [0] + list(map(int, input().split()))

  tmp = m
  flag = True

  for i in range(1, n+1):
    tmp -= h_list[i]
    if tmp < 0:
      flag = False
      print(i-1)
      break

  if flag:
    print(n)

if __name__ == "__main__":
  main()