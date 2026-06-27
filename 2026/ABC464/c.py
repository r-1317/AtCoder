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

  imos_list = [[] for _ in range(M)]  # 時間が外側、色が内側

  for _ in range(N):
    a, d, b, = map(int, input().split())
    a -= 1
    d -= 1
    b -= 1
    imos_list[0].append((a, 1))
    imos_list[d].append((a, -1))
    imos_list[d].append((b, 1))

  colour_list = [0]*N
  count = 0

  for i in range(M):
    for c, dc in imos_list[i]:
      colour_list[c] += dc
      if colour_list[c] == 0:  # 色が減った場合
        count -= 1
      elif colour_list[c] == 1 and dc == 1:
        count += 1
    
    print(count)


if __name__ == "__main__":
  main()