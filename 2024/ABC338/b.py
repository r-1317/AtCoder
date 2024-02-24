import collections

def str2list(s):
  list_s = [""]*len(s)
  for i in range(len(s)):
    list_s[i] = s[i]

  return list_s

def main():
  s = input()
  s_list = str2list(s)
  tmp = collections.Counter(s_list).most_common()  # 文字頻度

  max_list = [125]*len(s)
  max_list[0] = ord(tmp[0][0])
  tmp.append(("",0))
  i = 0

  while tmp[i][1] == tmp[i+1][1]:
    max_list[i+1] = ord(tmp[i+1][0])
    i += 1

  ans = chr(min(max_list))

  print(ans)
  # print(tmp)
  # print(max_list)

if __name__ == "__main__":
  main()