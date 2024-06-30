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
  s, t = input().split()

  flag = False

  # sをi文字ごとに切り出す
  for i in range(1,len(s)):
    tmp_list = []
    for j in range(len(s)//i+1):
      tmp_list.append(s[j*i:(j+1)*i])
    ic(tmp_list)

    for j in range(i):
      tmp = ""
      for k in range(len(tmp_list)):
        if j < len(tmp_list[k]):
          tmp += tmp_list[k][j]
      ic(tmp)
      if tmp == t:
        flag = True
        break

  print("Yes" if flag else "No")

if __name__ == "__main__":
  main()