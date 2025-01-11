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
  a_list = list(map(int, input().split()))

  shortage = 0  # すでに途絶えた供給の数
  shortage_dict = {}  # i番目を最後に途絶える供給の数
  for i in range(n):
    a_list[i] += i - shortage
    # 足りる場合
    if (n-1-i) <= a_list[i]:
      a_list[i] -= (n-1-i)
    # 足りない場合
    else:
      end_i = i + a_list[i]
      if end_i in shortage_dict:
        shortage_dict[end_i] += 1
      else:
        shortage_dict[end_i] = 1
      a_list[i] = 0
    # shortageの更新
    if i in shortage_dict:
      shortage += shortage_dict[i]
    ic(a_list, shortage, shortage_dict)

  print(*a_list)


if __name__ == "__main__":
  main()