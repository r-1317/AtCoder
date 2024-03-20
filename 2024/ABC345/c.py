from icecream import ic

def main():
  s = input()
  if len(s) % 2 == 1:
    ans = len(s) * ((len(s)-1)//2)
  else:
    ans = len(s) * ((len(s)-2)//2 + 1)

  # ic(ans)
  freq = -26

  for i in range(26):
    tmp = s.count(chr(97+i))

    if tmp % 2 == 1:
      freq += tmp * ((tmp-1)//2)
    else:
      freq += tmp * ((tmp-2)//2 + 1)

    if tmp <= 1:
      freq += 1

  # ic(freq)

  print(ans - freq)


if __name__ == "__main__":
  main()