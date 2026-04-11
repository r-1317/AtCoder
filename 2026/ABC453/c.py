import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def sign(x):
  return 1 if abs(x) == x else -1

def main():
  N = int(input())
  l_list = list(map(int, input().split()))

  max_count = -1

  for bits in range(2**N):
    pos = 0.5
    count = 0
    for i in range(N):
      fugou = int(bits >> i & 1)
      fugou = 1 if fugou else -1  # 応急処置
      l = l_list[i]
      next_pos = pos + l  * fugou
      # ic(fugou)
      if sign(next_pos) != sign(pos):
        count += 1
      pos = next_pos
    max_count = max(max_count, count)

  print(max_count)



if __name__ == "__main__":
  main()