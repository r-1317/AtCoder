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
  N = int(input())

  a_b_list = [list(map(int, input().split())) for _ in range(N)]

  M = int(input())

  s_list = [list(input()) for _ in range(M)]  # 文字列をlistとしたやつのlist

  chr_idx_list = [[] for _ in range(11)]  # 長さiでj文字目がkの単語があるか

  for i in range(11):
    chr_idx_list[i] = [[False]*26 for _ in range(i)]

  for s in s_list:
    for i in range(len(s)):
      c = s[i]
      chr_idx_list[len(s)][i][ord(c)-97] = True

  ic(chr_idx_list[5][1][17])

  for i in range(M):
    spine = s_list[i]
    if len(spine) != N:
      ans = "No"
      ic(ans)
      print(ans)
      continue
    flag = True
    for j in range(len(spine)):
      a, b = a_b_list[j]
      c = spine[j]
      if not chr_idx_list[a][b-1][ord(c)-97]:
        ic(a, b, c)
        flag = False
    ans = "Yes" if flag else "No"
    ic(ans, spine)
    print(ans)


if __name__ == "__main__":
  main()