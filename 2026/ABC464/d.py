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
  T = int(input())

  for _ in range(T):
    N = int(input())
    S = input()

    weathers = [0 if S[i] == "S" else 1 for i in range(N)]  # スペルがあっているかは知らん
    ic(weathers)

    x_list = list(map(int, input().split()))
    y_list = list(map(int, input().split()))  # あとから足す方式

    dp_list = [[0, 0] for _ in range(N)]

    dp_list[0][int(not(weathers[0]))] -= x_list[0]  # 初日の天気を変更

    for i in range(1, N):
      if weathers[i] == 0:  # もとが晴れの場合
        dp_list[i][0] = max(dp_list[i-1][0], dp_list[i-1][1] + y_list[i-1])
        dp_list[i][1] = max(dp_list[i-1][0], dp_list[i-1][1]) - x_list[i]
      else:  # もとが雨の場合
        dp_list[i][0] = max(dp_list[i-1][0], dp_list[i-1][1] + y_list[i-1]) - x_list[i]
        dp_list[i][1] = max(dp_list[i-1][0], dp_list[i-1][1])

    print(max(dp_list[-1]))

if __name__ == "__main__":
  main()