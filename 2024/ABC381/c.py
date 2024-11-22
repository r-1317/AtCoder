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
  n = int(input())
  s_list = list(input())

  max_count = 0

  one_count = 0
  two_count = 0
  tmp = ""

  for i, x in enumerate(s_list):
    # 直前が11/22文字列になりえない場合
    if tmp == "":
      if x == "1":
        one_count += 1
        tmp = "1"
      elif x == "/":
        tmp = "2"

    # 直前が111/22文字列の1部分の場合
    elif tmp == "1":
      if x == "1":
        one_count += 1
      elif x == "/":
        tmp = "2"
      elif x == "2":  # リセット
        one_count = 0
        two_count = 0
        tmp = ""

    # 直前が111/22文字列の2部分の場合
    elif tmp == "2":
      if x == "2":
        two_count += 1
      else:  # 部分文字列が完成し、リセット
        max_count = max(max_count, min(one_count, two_count)*2+1)
        one_count = 0
        two_count = 0
        tmp = ""

    ic(i, x, one_count, two_count, tmp)

  if tmp == "2":
    max_count = max(max_count, min(one_count, two_count)*2+1)

  print(max_count)


if __name__ == "__main__":
  main()