def main():
  ans = 0
  for _ in range(100):
    S = input()
    ans += int(S[11:])

  print(ans)

if __name__ == "__main__":
  main()