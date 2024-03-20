from icecream import ic

def main():
  x = int(input())
  if str(x)[-1] == "0" or x < 0:
    if x == 0 or x == -1:
      print(0)
    else:
      print(str(x)[:-1])
  else:
    if x == 1:
      print(1)
    else:
      print(int(str(x)[:-1])+1)

if __name__ == "__main__":
  main()