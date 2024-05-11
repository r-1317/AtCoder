from icecream import ic

def main():
  s = "0" + input()
  t = "0" + input()

  len_s = len(s)

  ans = [0]*len_s
  count = 1

  for i in range(1, len(t)+1):

    if t[i] == s[count]:
      ans[count - 1]  += i
      count += 1

      if count == len_s:
        break

  ans = ans[:-1]

  print(*ans)

if __name__ == "__main__":
  main()