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
    N, M = map(int, input().split())
    a_list = list(map(int, input().split()))

    ans = 0

    # 均等に入れる
    for i in range(M):
      a = a_list[i]
      ans += 2**a * (a // N)
      a_list[i] = a % N

    # 合成する
    for i in range(M-1, 0, -1):
      num_list = [0]*(i+1)  # 合成に必要な個数のリスト
      num_list[i] = N - a_list[i]
      w = 2**i * (N - a_list[i])
      for j in range(i-1, -1, -1):
        if 2**j * (a_list[j]) >= w:  # ここで終われる場合
          w = 0
          num_list[j] = w // 2**j  # 個数
          break
        w -= 2**j * a_list[j]
        num_list[j] = a_list[j]

      # ここから合成の処理
      if w > 0:  # 合成で届かない場合はやらない
        continue
      for j in range(i):
        a_list[i] -= num_list[i]
      ans += 2**i

    # この時点ですべての合成が終わったはず
    # あとはそのときの現存する最大値を入れたらいい?
    for i in range(i, -1, -1):
      if a_list[i] > 0:
        ans += 2**i

    ic(ans)
    print(ans)

if __name__ == "__main__":
  main()