from icecream import ic

def main():
  tmp = 1  # 初期値は0でなければ何でも良い
  a_list = []

  # 0が来るまで繰り返す
  while tmp != "0":
    tmp = input()  # 数字(文字列型)
    a_list.append(tmp)

  # ic(a_list)

  a_list.reverse()

  # ic(a_list)

  print("\n".join(a_list))


if __name__ == "__main__":
  main()