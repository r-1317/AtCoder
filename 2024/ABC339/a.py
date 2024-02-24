def main():

  s = input()
  n = s.rfind(".")
  ans = s[n+1:]

  print(ans)

if __name__ == "__main__":
  main()