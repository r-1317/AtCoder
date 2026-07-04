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
  N = int(input())
  S = input()

  a_list = list(range(1, N+1))

  l = 0
  r = N-1

  ans_list = [-1]*N

  cur = 1  # 右からの意

  for i in range(N-1, -1, -1):  # 逆順
    if S[i] == "o":
      cur = not(cur)  # 反転
    
    if cur:
      ans_list[i] = a_list[r]
      r -= 1
    else:
      ans_list[i] = a_list[l]
      l += 1

  print(*ans_list)

if __name__ == "__main__":
  main()