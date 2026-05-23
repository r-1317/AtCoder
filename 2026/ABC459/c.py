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
  N, Q = map(int, input().split())

  remove_count = 0
  towers = [0]*N
  counts = [0]*(10**6)
  counts[0] = N

  for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 1:
      x = query[1]
      x -= 1
      towers[x] += 1
      counts[towers[x]] += 1
      if counts[remove_count+1] == N:
        remove_count += 1
    else:
      y = query[1]
      print(counts[y + remove_count])


if __name__ == "__main__":
  main()