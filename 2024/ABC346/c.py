from icecream import ic

def main():
  n, k = map(int, input().split())
  a_list = list(map(int, input().split()))
  a_list = list(set(a_list))
  a_list.sort()
  ans = (k * (k+1)) //2

  # ic(ans)  # デバッグ
  # ic(a_list)  # デバッグ

  for a in a_list:
    if k < a:
      break
    else:
      ans -= a

  print(ans)

if __name__ == "__main__":
  main()