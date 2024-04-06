from icecream import ic

def main():
  n, k = map(int, input().split())
  a_list = list(map(int, input().split()))
  ans = ""

  for a in a_list:
    if a % k == 0:
      ans += f"{a // k} "

  print(ans[:-1])


if __name__ == "__main__":
  main()