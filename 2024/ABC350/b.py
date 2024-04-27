from icecream import ic

def main():
  n, q = map(int, input().split())
  t_list = list(map(int, input().split()))  # 治療する歯のリスト
  teeth_list = [True]*(n+1)  # 穴の番号とリストのindexは対応する
  teeth_list[0] = False  # 0番目の要素は常にFalseであり、無視する

  for t in t_list:
    if teeth_list[t]:
      teeth_list[t] = False
    else:
      teeth_list[t] = True

  ans = 0

  for tooth in teeth_list:
    if tooth:
      ans += 1

  print(ans)

if __name__ == "__main__":
  main()