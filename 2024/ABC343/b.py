from icecream import ic
# ic.disable()

def main():
  n = int(input())  # 頂点の数

  # 行のループ
  for _ in range(n):
    a_list = list(map(int, input().split()))
    ans = ""

    # 列のループ
    for i in range(n):
      if a_list[i] == 1:
        ans += f"{i+1} "

    # 末尾の空白を削除
    if len(ans) != 0:
      ans = ans[:-1]

    print(ans)

if __name__ == "__main__":
  main()