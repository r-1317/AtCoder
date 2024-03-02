from icecream import ic
# ic.disable()

def main():
  n, t = map(int, input().split())
  scores = [[0]*n for _ in range(t)]  # 選手ごと、時刻ごとの得点

  a_b = [list(map(int, input().split())) for _ in range(t)]

  # 選手ごと、時刻ごとの得点を計算
  for i in range(t):

    # 前の得点を引き継ぐ
    if i != 0:
      scores[i] = scores[i-1][:]

    # i + 0.5 秒後の得点を加算
    scores[i][a_b[i][0] -1] += a_b[i][1]

  for i in range(t):
    print(len(set(scores[i])))

  # ic(scores)



if __name__ == "__main__":
  main()

#score[a-1] += b
#print(len(set(score)))