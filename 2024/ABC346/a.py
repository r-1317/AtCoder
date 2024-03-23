from icecream import ic

def main():
  n = int(input())
  a_list = list(map(int, input().split()))
  ans = ""

  for i in range(len(a_list)-1):
    b = a_list[i]*a_list[i+1]
    ans += f"{b} "

  print(ans[:-1])

if __name__ == "__main__":
  main()