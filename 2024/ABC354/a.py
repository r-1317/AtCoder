from icecream import ic

def main():
  h = int(input())

  p_height = 0

  days = 0

  while p_height <= h:
    p_height += 2 ** days
    days += 1

  print(days)

if __name__ == "__main__":
  main()