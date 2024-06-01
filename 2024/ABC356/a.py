from icecream import ic

def main():
  n, l, r = map(int, input().split())

  a_list = [0]*n

  for i in range(n):
    a_list[i] = i+1

  b_list = [0]*(r-l+1)
  i = 0

  for b in range(r, l-1, -1):
    b_list[i] = b
    i += 1

  # ic(a_list)
  # ic(b_list)

  for i in range(len(b_list)):
    a_list[l-1+i] = b_list[i]

  # ic(a_list)

  print(*a_list)


if __name__ == "__main__":
  main()