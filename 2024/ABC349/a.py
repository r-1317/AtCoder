from icecream import ic

def main():
  n = int(input())
  a_list = list(map(int, input().split()))  # 要素数n-1

  print(0 - sum(a_list))


if __name__ == "__main__":
  main()