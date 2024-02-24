def main():
  n, m, k = map(int, input().split())
  count_n = count_m = 0
  n_ans_list = [-1] * k
  m_ans_list = [-1] * k


  for i in range(1,10**18):

    if m == 1:
      break

    tmp = i*n

    if not tmp%m == 0:
      n_ans_list[count_n] = tmp
      count_n += 1

      if count_n == k:
        break

  print("n終わり")

  for i in range(1,10**18):

    if n == 1:
      break

    tmp = i*m

    if not tmp%n == 0:
      m_ans_list[count_m] = tmp
      count_m += 1

      if count_m == k:
        break

  print("m終わり")

  # ans_list = n_ans_list + m_ans_list
  ans_list = [ans for ans in n_ans_list if ans != -1] + [ans for ans in m_ans_list if ans != -1]
  # print(ans_list)  # デバッグ

  for i in range(k-1):
    ans = ans_list.pop(min(ans_list))

  # print(ans_list)  # デバッグ

  print(ans)



if __name__ == "__main__":
  main()