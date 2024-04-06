from icecream import ic

def main():
  n = int(input())
  # a_c_list = [list(map(int, input().split())) for _ in range(n)]
  dict = {}  # 色ごとの最小のおいしさ

  # 豆iについて検証
  for i in range(n):
    a, c = map(int, input().split())

    if c in dict:
      dict[c] = min(a, dict[c])
    else:
      dict[c] = a

  # ic(dict)

  print(max(dict.values()))

if __name__ == "__main__":
  main()