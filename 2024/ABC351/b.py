from icecream import ic

def main():
  n = int(input())
  a_list = [(input()) for _ in range(n)]  # 2次元配列ではない
  b_list = [(input()) for _ in range(n)]

  # ic(a_list)
  # ic(b_list)

  for i in range(n):  # i: 行
    for j in range(n):  # j: 列

      if a_list[i][j] != b_list[i][j]:
        print(f"{i+1} {j+1}")


if __name__ == "__main__":
  main()