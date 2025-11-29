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
  S = input()
  s_list = list(S)
  N = len(S)

  for i in range(N):
    s_list[i] = int(s_list[i])

  count_list = []  # [(数字, 回数), ...]

  current_num = s_list[0]
  num_count = 0
  for i in range(N):
    if s_list[i] == current_num:
      num_count += 1
    else:
      count_list.append((current_num, num_count))
      current_num = s_list[i]
      num_count = 1

  count_list.append((current_num, num_count))

  ic(count_list)

  ans = 0

  for i in range(len(count_list) - 1):
    a = count_list[i][0]
    b = count_list[i+1][0]
    if a + 1 != b:
      continue
    ans += min(count_list[i][1], count_list[i+1][1])

  print(ans)



if __name__ == "__main__":
  main()