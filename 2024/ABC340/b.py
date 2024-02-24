
def main():
  q = int(input())  # クエリの数
  A = []

  for i in range(q):

    q_type, tmp = map(int, input().split())  # "1"or"2", "x" or "k"

    # クエリが1の場合
    if q_type == 1:
      A.append(tmp)

    # クエリが2の場合
    else:
      print(A[-tmp])




if __name__ == "__main__":
  main()