from icecream import ic

def debug_200000():
  s = ""

  for i in range(1,200001):
    s += str(i) + " "

  return list(map(int, s[:-1].split()))

def is_possible(a_list, b_list, c_list, x):

  possibility = False

  for a in a_list:
    sum = a
    if x < sum:
      break

    for b in b_list:
      sum += b
      if x < sum:
        break

      for c in c_list:
        sum += c
        if sum == x:
          possibility = True
          # ic(x)
          # ic(sum)
          break
        elif x < sum:
          # ic(x)
          # ic(sum)
          break

  return possibility

def calc_sum(a_list, b_list, c_list):
  sum_set = set()

  for a in a_list:
    for b in b_list:
      for c in c_list:
        sum_set.add(a+b+c)

  # ic(sum_set)
  return sum_set

def main():
  n = int(input())
  a_list = sorted(list(map(int, input().split())))

  m = int(input())
  b_list = sorted(list(map(int, input().split())))

  l = int(input())
  c_list = sorted(list(map(int, input().split())))

  q = int(input())
  x_list = list(map(int, input().split()))
  # x_list = debug_200000()

  sum_set = calc_sum(a_list, b_list, c_list)

  for x in x_list:
    if x in sum_set:
      print("Yes")
    else:
      print("No")

if __name__ == "__main__":
  main()