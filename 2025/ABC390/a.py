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
  a_list = list(map(int, input().split()))
  sorted_a_list = sorted(a_list)

  flag = False

  for i in range(len(a_list)-1):
    tmp_list = a_list[:]
    tmp_list[i], tmp_list[i+1] = tmp_list[i+1], tmp_list[i]
    if tmp_list == sorted_a_list:
      flag = True
      break

  print("Yes" if flag else "No")

if __name__ == "__main__":
  main()