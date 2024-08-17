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
  n, k = map(int, input().split())
  r_list = list(map(int, input().split()))

  len_a_list = 1

  for r in r_list:
    len_a_list *= r

  ic(len_a_list)

  a_list = [[0]*n for _ in range(len_a_list)]

  ic(a_list)

  for i in range(n):
    a_list[0][i] = 1

  ic(a_list)

  for i in range(1, len_a_list):
    tmp = n-1
    while True:
      ic(tmp)
      if a_list[i-1][tmp] < r_list[tmp]:
        break
      tmp -= 1
    
    ic(tmp)

    a_list[i] = a_list[i-1][:]

    a_list[i][tmp] += 1

    for j in range(tmp+1, n):
      a_list[i][j] = 1

    ic(a_list)

  ic(len(a_list))

  for a in a_list:
    # ic(a)
    # ic(sum(a))
    if sum(a) % k == 0:
      print(*a)

if __name__ == "__main__":
  main()