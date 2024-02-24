
def main():
  n = int(input())  # 文字数
  s = input()  # もとの文字列
  q = int(input())  # 操作の回数
  ans = ""

  mapping_to = "abcdefghijklmnopqrstuvwxyz"

  for _ in range(q):
    c, d = input().split()
    mapping_to = mapping_to.replace(c, d) # c を d に置き換える

  for i in range(n):
    ans += mapping_to[ord(s[i]) - 97]


  print(ans)

if __name__ == "__main__":
  main()
