from icecream import ic

def main():
  s = input()
  s_middle = s[1:-1]
  # ic(s_middle)
  ans = True
  if s[0] == "<" and s[-1] == ">":
    for i in range(len(s_middle)):
      if s_middle[i] != "=":
        ans = False
  else:
    ans = False

  if ans:
    print("Yes")
  else:
    print("No")

if __name__ == "__main__":
  main()