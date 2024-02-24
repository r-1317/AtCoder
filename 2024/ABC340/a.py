
def main():
  a, b, d = map(int, input().split())  # 初項, 末項, 公差
  ans = ""

  for i in range(a,b+1,d):
    ans += str(i) + " "

  ans = ans[:-1]

  print(ans)

if __name__ == "__main__":
  main()