from icecream import ic

def min_not_0(d_list):
  d_list.sort()

  if d_list[0] == 0:
    return False, 0
  else:
    return True, d_list[0]

def main():
  n, a, b = map(int, input().split())
  d_list = list(map(int, input().split()))

  for i in range(n):
    d_list[i] = d_list[i] % (a+b)  # 週のループをすべて1週目に
  d_list.sort()

  # ic(d_list)

  week_start = d_list[0]
  for i in range(n):
    d_list[i] -= week_start

  d_list.sort()
  # ic(d_list)


  if d_list[-1] < a:
    print("Yes")
  else:
    print("No")


if __name__ == "__main__":
  main()