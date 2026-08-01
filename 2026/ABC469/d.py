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
  N, M = map(int, input().split())
  A, B = map(int, input().split())  # 最初の組
  A_pair = [i if i != A else 10**9 for i in range(1, N+1)]  # Aのペアになる可能性のあるプレイヤーの配列。
  A_pair.sort()
  A_pair.pop()  # 末尾を削除
  B_pair = [i if i != B else 10**9 for i in range(1, N+1)]  # Bのペアになる可能性のあるプレイヤーの配列。
  B_pair.sort()
  B_pair.pop()  # 末尾を削除

  for i in range(M-1):
    a, b = map(int, input().split())
    if A not in (a, b):
      new_A_pair = []
      for x in A_pair:
        if x in (a, b):
          new_A_pair.append(x)
      A_pair = new_A_pair
    if B not in (a, b):
      new_B_pair = []
      for x in B_pair:
        if x in (a, b):
          new_B_pair.append(x)
      B_pair = new_B_pair

  ans = 0
  ans += len(A_pair)
  ans += len(B_pair)
  if A in B_pair and B in A_pair:
    ans -= 1

  print(ans)

  ic(A_pair)
  ic(B_pair)

if __name__ == "__main__":
  main()