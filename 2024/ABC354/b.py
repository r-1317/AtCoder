from icecream import ic

def main():
  n = int(input())
  s_c_list = [list(input().split()) for _ in range(n)]  # cもstr型で受け取る

  s_list = [""]*n  # 名前のリスト
  c_sum = 0  # 問題文で言うT

  for i in range(n):
    s_list[i] = s_c_list[i][0]
    c_sum += int(s_c_list[i][1])

  s_list.sort()

  number = c_sum%n

  print(s_list[number])

if __name__ == "__main__":
  main()