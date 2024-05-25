from icecream import ic

def main():
  a, b = map(int, input().split())
  if a == b:
    print(-1)
  else:
    print(6-a-b)

if __name__ == "__main__":
  main()