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
  s = input()  # キーボードの文字列
  ans = 0  # 指の移動距離
  tmp = s.find("A")  # 現在の指の位置
  ic(tmp)

  for i in range(1,26):
    ic(chr(65+i))
    dist = abs(tmp - s.find(chr(65+i)))  # 指の移動距離
    ic(s.find(chr(65+i)), dist)
    ans += dist
    tmp = s.find(chr(65+i))

  print(ans)

if __name__ == "__main__":
  main()