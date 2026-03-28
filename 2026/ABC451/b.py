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
  current_nums = [0]*M
  next_nums = [0]*M
  for _ in range(N):
    a, b = map(int, input().split())
    current_nums[a-1] += 1
    next_nums[b-1] += 1

  for i in range(M):
    print(next_nums[i] - current_nums[i])

if __name__ == "__main__":
  main()