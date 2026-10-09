def main():
  ans = 0
  for _ in range(100):
    row = input().split()
    ans += int(row[1])

  print(ans)

if __name__ == "__main__":
  main()