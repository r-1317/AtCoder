from icecream import ic

def main():
  n = int(input())
  h_list = list(map(int, input().split()))

  ans = -1

  for i in range(1,n):
    if h_list[0] < h_list[i]:
      ans = i+1
      break

  print(ans)

if __name__ == "__main__":
  main()