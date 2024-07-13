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
  n, k = map(int, input().split())
  a_list = list(map(int, input().split()))

  a_list.sort()
  ic(a_list)

  ans = 10**9

  for head in range(k+1):
    tail = n - k + head - 1

    ic(head, tail)

    ans = min(ans, a_list[tail] - a_list[head])

    # ic(a_list[head:tail+1], ans)  # こいつのせいでTLEしたのか？

  print(ans)

if __name__ == "__main__":
  main()