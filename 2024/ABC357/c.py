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

  carpets = [""]*7
  carpets[0] = "#"

  # カーペットの初期化
  for i in range(1, 7):
    carpets[i] = [[""]*(3**i) for _ in range(3**i)]

  ic(carpets[0])

  # カーペットの作成
  for i in range(1, n+1):
    for j in range(3**i):  # 縦
      for k in range(3**i):  # 横
        ic(i,j,k)

        if 3**(i-1) <= j < 2*3**(i-1) and 3**(i-1) <= k < 2*3**(i-1):
          carpets[i][j][k] = "."
        else:
          carpets[i][j][k] = carpets[i-1][j%3**(i-1)][k%3**(i-1)]

  ic(carpets[n])

  ans = "\n".join(["".join(carpets[n][i]) for i in range(3**n)])

  print(ans)

if __name__ == "__main__":
  main()