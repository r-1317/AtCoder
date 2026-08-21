import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def find_i(x, R):
  max_i = 61
  for i in range(62):
    if x >> i & 1:
      max_i = i
      break

  for i in range(max_i, -1, -1):
    j = x // 2**i
    if 2**i * (j+1) <= R:
      ic(x, i, j)
      ic(2**i * j)
      return i

def main():
  L, R = map(int, input().split())

  x = L

  ans_list = []

  while x < R:
    i = find_i(x, R)
    j = x // 2**i
    new_x = 2**i * (j+1)
    ans_list.append((x, new_x))
    ic(i, j)
    ic(bin(x))
    x = new_x

  print(len(ans_list))
  for row in ans_list:
    print(*row)



if __name__ == "__main__":
  main()