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
  n, t, p = map(int, input().split())
  l_list = list(map(int, input().split()))

  for i in range(n):
    l_list[i] -= t

  l_list.sort(reverse=True)

  ic(l_list)

  if l_list[p-1] < 0:
    print(abs(l_list[p-1]))
  else:
    print(0)

if __name__ == "__main__":
  main()