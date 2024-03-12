from icecream import ic

def main():
  s = input()
  first = s.find("|")
  second = s.rfind("|")

  # ic(first)
  # ic(second)


  s = s[:first] + s[second+1:]

  # ic(s[:first])
  # ic(s[second+1:])

  print(s)

if __name__ == "__main__":
  main()