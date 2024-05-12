from icecream import ic

def main():
  n, k = map(int, input().split())
  a_list = list(map(int, input().split()))

  ans = 0
  tmp = 0

  for i in range(n):
    if tmp + a_list[i] <= k:
      tmp += a_list[i]
    else:
      ans += 1
      tmp = a_list[i]

  if tmp:
    ans += 1

  print(ans)

if __name__ == "__main__":
  main()