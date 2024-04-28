from icecream import ic

def main():
  a_list = list(map(int, input().split()))
  b_list = list(map(int, input().split()))

  a_sum = 0
  b_sum = 0

  for a in a_list:
    a_sum += a

  for b in b_list:
    b_sum += b

  # ic(a_sum)
  # ic(b_sum)

  print(a_sum - b_sum + 1)

if __name__ == "__main__":
  main()