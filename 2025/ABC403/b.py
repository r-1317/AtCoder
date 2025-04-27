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
  t_list = list(input())
  u_list = list(input())

  for i in range(len(t_list) - len(u_list) + 1):
    flag = True
    for j in range(len(u_list)):
      ic(i, j, t_list[i + j], u_list[j])
      ic(t_list[i + j] != u_list[j] or t_list[i + j] == "?")
      if not(t_list[i + j] == u_list[j] or t_list[i + j] == "?"):
        flag = False
        break
    ic(i, flag)
    if flag:
      print("Yes")
      exit()

  print("No")

if __name__ == "__main__":
  main()