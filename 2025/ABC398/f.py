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
  s_list = list(input())

  min_i = len(s_list)
  for i in range(len(s_list)):
    flag = True
    for j in range((len(s_list)-i)//2):
      if s_list[i+j] != s_list[-1-j]:
        flag = False
        break
    if flag:
      min_i = i
      break

  t_list = s_list[:min_i]
  t_list.reverse()
  ic(min_i, t_list)

  ans_list = s_list + t_list

  print(*ans_list, sep="")

if __name__ == "__main__":
  main()