import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  n, k = map(int, input().split())
  s = input()
  s_list = list(s)
  s_list.append("?")  # 末尾に?を追加
  s_list = ["?"] + s_list  # 先頭に?を追加

  for i in range(1, n + 1):
    if s_list[i] == "o":
      s_list[i-1] = "."
      s_list[i+1] = "."

  s_list = s_list[1:-1]  # 先頭と末尾の?を削除

  t_list = s_list[:]

  o_count = 0

  hatena_start = None
  flag = False
  for i in range(n):
    if s_list[i] == "o":
      o_count += 1
    elif s_list[i] == "?":
      if not flag:
        hatena_start = i
        flag = True
      else:
        o_count += (i - hatena_start) // 2
        if (i - hatena_start) % 2:
          o_count += 1
        hatena_start = None
        flag = False

  ic(o_count)

  if o_count == k:
    for i in range(n):
      if t_list[i] == "?":
        t_list[i] = "."
        print(*t_list, sep="")
        exit()

  hatena_start = None
  flag = False
  for i in range(n):
    if t_list[i] == "?":
      if not flag:
        hatena_start = i
        flag = True
      elif (i - hatena_start) % 2:
        for j in range(hatena_start, i+1):
          if j%2:
            t_list[j] = "."
          else:
            t_list[j] = "o"
        hatena_start = None
        flag = False

  if o_count == k:
    print(*t_list, sep="")
  else:
    print(*s_list, sep="")

if __name__ == "__main__":
  main()