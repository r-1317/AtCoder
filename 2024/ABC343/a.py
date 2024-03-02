from icecream import ic
# ic.disable()

def main():
  a, b = map(int, input().split())
  if a == 0 and b == 0:
    print("1")
  else:
    print("0")

if __name__ == "__main__":
  main()