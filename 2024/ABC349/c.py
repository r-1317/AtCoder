from icecream import ic

def main():
  s = input()  # 空港名
  t = input().lower()  # 空港コード(小文字化)

  flag = True

  # ic(s)
  # ic(t[0])

  # 1文字目
  if t[0] in s:
    s = s[s.find(t[0])+1:]  # 1文字目以前の切り捨て
  else:
    flag = False

  # ic(s)
  # ic(flag)

  # 2文字目
  if t[1] in s:
    s = s[s.find(t[1])+1:]  # 2文字目以前の切り捨て
  else:
    flag = False

  # ic(s)
  # ic(flag)

  # 3文字目
  if t[2] != "x":
    if t[2] in s:
      s = s[s.find(t[2])+1:]  # 3文字目以前の切り捨て
    else:
      flag = False

  if flag:
    print("Yes")
  else:
    print("No")


if __name__ == "__main__":
  main()