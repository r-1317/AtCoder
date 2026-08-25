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
  a_b_list = [list(map(int, input().split())) for _ in range(N)]

  point_list = [-1]*(2*N)
  for i in range(N):
    a, b = a_b_list[i]
    a -= 1
    b -= 1
    point_list[a] = i
    point_list[b] = i
  ic(point_list)

  ans = False
  visited_list = [False]*N
  stack = []
  for p in point_list:
    if not visited_list[p]:
      stack.append(p)
      visited_list[p] = True
    else:
      if stack[-1] != p:
        ans = True
        break
      stack.pop()

  print("Yes" if ans else "No")

if __name__ == "__main__":
  main()