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
  num_count_list = [[] for _ in range(n)]
  num_list = [[] for _ in range(n)]
  k_list = [0]*n
  for i in range(n):
    in_list = list(map(int, input().split()))
    k_list[i] = in_list[0]
    tmp_list = [0]*(10**5+1)
    for j, a in enumerate(in_list):
      if j == 0:
        continue
      if tmp_list[a] == 0:
        num_list[i].append(a)
      tmp_list[a] += 1
    num_count_list[i] = tmp_list
  ic(num_list)
  num_set_list = [set(num_list[i]) for i in range(n)]

  match_list = [[0]*n for _ in range(n)]
  for i in range(n):
    for a in num_list[i]:
      for j in range(n):
        if i == j:
          continue
        if a in num_set_list[j]:
          match_list[i][j] += (num_count_list[i][a] / k_list[i]) * (num_count_list[j][a] / k_list[j])
  
  max_prob = -1
  for i in range(n):
    for j in range(n):
      if i == j:
        continue
      max_prob = match_list[i][j] if max_prob < match_list[i][j] else max_prob
  print(max_prob)


if __name__ == "__main__":
  main()