from icecream import ic

def main():
  n, m = map(int, input().split())
  a_list = list(map(int, input().split()))
  b_list = list(map(int, input().split()))

  a_set = set(a_list)
  b_set = set(b_list)

  a_b_list = list(a_set | b_set)
  a_b_list.sort()

  # ic(a_b_list)

  flag = False

  for i in range(n+m-1):
    if a_b_list[i] in a_set and a_b_list[i+1] in a_set:
      flag = True
      break

  print("Yes" if flag else "No")


if __name__ == "__main__":
  main()