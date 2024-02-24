
def main():
  n = int(input())  # 列の人数
  p_list = list(map(int, input().split()))  # 人の列
  q = int(input())  # クエリの数

  for _ in range(q):
    a, b = map(int, input().split())

    # indexが小さい方を出力
    if p_list.index(a) < p_list.index(b):
      print(a)
    else:
      print(b)


if __name__ == "__main__":
  main()