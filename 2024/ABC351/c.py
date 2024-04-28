from icecream import ic

def main():
  n = int(input())
  a_list = [0] + list(map(int, input().split()))
  ball_list = [-1]*(n+1)
  ball_count = 0

  # 操作開始
  for i in range(1, n+1):

    ball_list[ball_count+1] = a_list[i]
    ball_count += 1

    while ball_list[ball_count - 1] == ball_list[ball_count]:

      ball_list[ball_count - 1] += 1
      ball_list[ball_count] = 0  # 別に必要な処理ではない

      ball_count -= 1


  print(ball_count)

if __name__ == "__main__":
  main()