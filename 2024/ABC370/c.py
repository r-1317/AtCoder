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
  s = input()  # もとの文字列
  t = input()  # 変換後の文字列

  x_list = []

  while s != t:
    tmp_list = []
    for i in range(len(s)):
      if s[i] != t[i]:
        tmp_s = s[:i] + t[i] + s[i+1:]
        tmp_list.append(tmp_s)
    tmp_list.sort(key=lambda x: list(x))
    ic(tmp_list)
    s = tmp_list[0]
    x_list.append(s)
    ic(s)
  
  print(len(x_list))
  for x in x_list:
    print(x)

if __name__ == "__main__":
  main()