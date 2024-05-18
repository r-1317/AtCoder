from icecream import ic

def main():
  n = int(input())
  a_c_list = [list(map(int, input().split()))+[True, i+1] for i in range(n)]  # [強さ, コスト, True, 番号]

  # ic(a_c_list)

  count = n
  a_c_list.sort(key=lambda x: x[1])
  a_list = [0]*n
  for i in range(n):
    a_list[i] = a_c_list[i][0]
  max_a = 0

  # ic(a_c_list)

  # 捨てるかどうかの判定
  for i in range(n):

    if a_c_list[i][0] < max_a:
      a_c_list[i][2] = False
      count -= 1

    else:
      max_a = a_c_list[i][0]

  # ic(a_c_list)

  # 回答の出力
  ans = [0]*count
  tmp = 0

  for i in range(n):
    if a_c_list[i][2]:
      ans[tmp] = a_c_list[i][3]
      tmp += 1

  ans.sort()

  print(count)
  print(*ans)


if __name__ == "__main__":
  main()