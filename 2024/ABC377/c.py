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
  n, m = map(int, input().split())
  a_b_list = [tuple(map(int, input().split())) for _ in range(m)]
  
  unsafe_set = set(a_b_list)
  ic(unsafe_set)
  move_list = [(2,1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2), (2,-1)]
  count = m

  for i in range(m):
    a, b = a_b_list[i]
    for x, y in move_list:
      if 0 < a + x <= n and 0 < b + y <= n:
        if (a + x, b + y) not in unsafe_set:
          count += 1
          unsafe_set.add((a + x, b + y))

  print(n**2 - count)

if __name__ == "__main__":
  main()