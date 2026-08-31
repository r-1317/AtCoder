import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def swap(u, i):
  dist = u.find("..")
  a =  u[i:i+2]
  if "." in a:
    return ""
  v = u[:i] + ".." + u[i+2:]
  v = v[:dist] + a + v[dist+2:]
  # ic(v)
  return v

def main():
  N = int(input())
  S = input() + ".."
  T = input() + ".."

  visited_set = set()

  ans = -1
  queue = [S]
  visited_set.add(S)
  for i in range(10**9):
    if T in visited_set:
      ans = i
      break
    if not queue:
      break
    new_queue = []
    for u in queue:
      for i in range(N+1):
        v = swap(u, i)
        if v and not v in visited_set:
          new_queue.append(v)
          visited_set.add(v)
    queue = new_queue

  print(ans)

if __name__ == "__main__":
  main()