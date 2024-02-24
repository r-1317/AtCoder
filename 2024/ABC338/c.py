
def main():
  n = int(input())
  qab_list = [list(map(int, input().split())) for _ in range(3)]
  q_list = qab_list[0]  # 持っている材料
  a_list = qab_list[1]  # aを作るのに必要な材料
  b_list = qab_list[2]  # bを作るのに必要な材料
  tmp_list = [0] * n
  flag_a = True
  flag_b = True
  num_a = 0
  num_b = 0
  ans = 0

  while flag_a:
    for i in range(n):

      tmp_list[i] = q_list[i] - a_list[i]*num_a

    if all(0 <= num for num in tmp_list) :
      pass
    else:
      num_a -= 1
      break

    while flag_b:
      for i in range(n):
        tmp_list[i] = q_list[i] - a_list[i]*num_a - b_list[i]*num_b
      
      if all(0 <= num for num in tmp_list) :
        ans = max(ans, num_a + num_b)
      else:
        num_b -= 1
        break

      num_b += 1
    
    num_a += 1

  # print(f"num_a: {num_a}")
  # print(f"num_b: {num_b}")
  print(ans)
  # print(num_a + num_b)


if __name__ == "__main__":
  main()