from icecream import ic

def main():
  s = input()
  n = int(s[3:])

  if 349 < n or n == 316 or n == 0:
    print("No")
  else:
    print("Yes")

if __name__ == "__main__":
  main()