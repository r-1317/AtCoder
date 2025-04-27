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
  n, d = map(int, input().split())
  a_list = list(map(int, input().split()))

  a_count = [0] * 10**6+1
  for a in a_list:
    a_count[a] += 1

  anti_a_count = [0] * 10**6+1

  for i in range(10**6+1):
    if a_count[i] == 0:
      continue
    if 1 <= i+d <= 10**6 and a_count[i+d]:
      anti_a_count[i+d] += a_count[i]
    if 1 <= i-d <= 10**6 and a_count[i-d]:
      anti_a_count[i-d] += a_count[i]

  sum_anti_a_count = 0
  for i in range(10**6+1):
    sum_anti_a_count += anti_a_count[i]
  ic(sum_anti_a_count)

  ans = 1

  sorted_i = list(range(10**6+1))
  sorted_i.sort(key=lambda x: anti_a_count[x], reverse=True)

  while sum_anti_a_count > 0:
    i = sorted_i.pop(0)
    if anti_a_count[i] == 0:
      continue
    sum_anti_a_count -= anti_a_count[i]
    ans += 1
    for j in range(10**6+1):
      if a_count[j] == 0:
        continue
      if 1 <= j+i <= 10**6 and a_count[j+i]:
        anti_a_count[j+i] -= a_count[j]
      if 1 <= j-i <= 10**6 and a_count[j-i]:
        anti_a_count[j-i] -= a_count[j]

if __name__ == "__main__":
  main()