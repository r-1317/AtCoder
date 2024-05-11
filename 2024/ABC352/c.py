from icecream import ic

def main():
  n = int(input())
  a_b_list = [list(map(int, input().split())) for _ in range(n)]   #a: 肩までの高さ, b: 頭までの高さ
  heads_list = [0]*n

  for i in range(n):
    heads_list[i] = a_b_list[i][1] - a_b_list[i][0]

  top = heads_list.index(max(heads_list))  # 頭の高さが最も高い人のindex

  # ic(top)

  ans = 0

  for i in range(n):
    ans += a_b_list[i][0]  # 肩までの高さの合計

  ans += a_b_list[top][1] - a_b_list[top][0]

  print(ans)

if __name__ == "__main__":
  main()