
cost = {0: 0, 1: 0}

def count_cost(x):

  if x in cost:
    return cost[x]
  
  half_x = x // 2
  # print(f"half_x: {half_x}")  # デバッグ
  
  tmp_1 = count_cost(half_x)
  tmp_2 = count_cost(x - half_x)
  # print(tmp_1,tmp_2)  # デバッグ

  cost[x] = tmp_1 + tmp_2 + x
  return cost[x]

def main():
  n = int(input())

  ans = count_cost(n)

  # print(cost)
  print(ans)

if __name__ == "__main__":
  main()