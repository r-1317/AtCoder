from icecream import ic

def main():
  n, k,  = map(int, input().split())
  p_list = [0] + list(map(int, input().split()))  # 0番目は無視

  pos_list = [0]*(n+1)  # 0番目は無視

  for i in range(1, n+1):
    pos_list[i] = p_list.index(i)  # i番目に数字iがある位置を格納

  # ic(pos_list)

  ans = 10**6

  for i in range(1, n+1-k):
    ans = min(ans, max(pos_list[i:i+k]) - min(pos_list[i:i+k]))

  print(ans)

if __name__ == "__main__":
  main()