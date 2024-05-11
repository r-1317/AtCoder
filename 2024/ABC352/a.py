from icecream import ic

def main():
  n, x, y, z = map(int, input().split())

  if x < z < y or y < z < x:
    print("Yes")
  else:
    print("No")

if __name__ == "__main__":
  main()