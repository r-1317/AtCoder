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
  N, L, R = map(int, input().split())
  p_list = list(map(int, input().split()))

  arr = []  # (点数, N - 出席番号)

  for i in range(N):
    p = p_list[i]
    arr.append((p, N-(i+1)))

  arr.sort(reverse=True)

  ans = -1

  for p, num in arr:
    if L <= p <= R:
      ans = num
      break

  print(-(ans-N) if ans != -1 else -1)

if __name__ == "__main__":
  main()