from icecream import ic

def main():
  s = input()
  freq_list = [0]*26  # 各文字の頻度

  # アルファベットの数だけ繰り返し
  for i in range(26):
    freq_list[i] = s.count(chr(i+97))

  # ic(freq_list)

  flag = True

  for i in range(1,101):

    if freq_list.count(i) != 0 and freq_list.count(i) != 2:
      flag = False

  if flag:
    print("Yes")
  else:
    print("No")

if __name__ == "__main__":
  main()