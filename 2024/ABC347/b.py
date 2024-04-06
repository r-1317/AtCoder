from icecream import ic

def main():
  s = input()
  s_set = set()

  for i in range(len(s)):
    for j in range(len(s) - i):
      s_set.add(s[j:j+i+1])

  print(len(s_set))

if __name__ == "__main__":
  main()