
def main():

  n = int(input())
  a_list = list(map(int, input().split()))  # 所持金のリスト

  for i in range(n-1):

    s, t = map(int, input().split())  #s: 支払う国iの通貨、t: 受け取る国i+1の通貨

    tmp = a_list[i] // s  # 操作の回数
    a_list[i+1] += t * tmp  # tmp回だけ加算

  print(a_list[-1])
  # print(a_list)  # デバッグ

if __name__ == "__main__":
  main()